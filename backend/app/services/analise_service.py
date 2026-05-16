import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.ia_service import generate_process_analysis
from app.repositories import analise_repository, diretriz_repository
from app.schemas.analise_schema import AnaliseIACreate
from app.models.processo import Processo
from app.models.etapa import Etapa
from app.models.conexao import Conexao

def request_analise(db: Session, processo_id: int):
    # Validar processo
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")

    # Buscar etapas
    etapas = db.query(Etapa).filter(Etapa.processo_id == processo_id).all()
    if not etapas:
        raise HTTPException(status_code=400, detail="O processo precisa ter pelo menos uma etapa para ser analisado.")

    # Buscar conexoes
    conexoes = db.query(Conexao).filter(Conexao.processo_id == processo_id).all()

    # Montar payload
    payload = {
        "processo": {
            "id": processo.id,
            "nome": processo.nome,
            "area": processo.area,
            "descricao": processo.descricao,
            "objetivo": processo.objetivo,
            "responsavel": processo.responsavel,
            "periodicidade": processo.periodicidade,
            "criticidade": processo.criticidade,
            "status": processo.status,
            "sistemas_utilizados": processo.sistemas_utilizados,
            "documentos_utilizados": processo.documentos_utilizados,
            "observacoes": processo.observacoes
        },
        "etapas": [
            {
                "id": e.id,
                "nome": e.nome,
                "descricao": e.descricao,
                "responsavel": e.responsavel,
                "entrada": e.entrada,
                "saida": e.saida,
                "sistema_utilizado": e.sistema_utilizado,
                "tempo_estimado": e.tempo_estimado,
                "tipo_etapa": e.tipo_etapa,
                "risco": e.risco,
                "gargalo": e.gargalo,
                "oportunidade_automacao": e.oportunidade_automacao,
                "posicao_x": e.posicao_x,
                "posicao_y": e.posicao_y
            } for e in etapas
        ],
        "conexoes": [
            {
                "id": c.id,
                "etapa_origem_id": c.etapa_origem_id,
                "etapa_destino_id": c.etapa_destino_id,
                "tipo_conexao": c.tipo_conexao,
                "condicao": c.condicao
            } for c in conexoes
        ],
        "metadados": {
            "total_etapas": len(etapas),
            "total_conexoes": len(conexoes),
            "fonte": "QDT Processos Contabeis",
            "tipo_analise": "mapeamento_processo_contabil"
        }
    }

    # Chamar IA
    analise_resultado = generate_process_analysis(payload)

    # Persistir Analise
    analise_create = AnaliseIACreate(
        processo_id=processo_id,
        resumo_executivo=analise_resultado.resumo_executivo,
        diagnostico_operacional=analise_resultado.diagnostico_operacional,
        nivel_maturidade=analise_resultado.nivel_maturidade.nivel if analise_resultado.nivel_maturidade else None,
        json_resultado=analise_resultado.model_dump_json()
    )
    db_analise = analise_repository.create_analise(db, analise_create)

    # Gerar Diretrizes
    diretrizes_data = []
    if analise_resultado.diretrizes_automacao:
        for d in analise_resultado.diretrizes_automacao:
            diretriz_data = {
                "processo_id": processo_id,
                "analise_id": db_analise.id,
                "titulo": d.titulo,
                "tipo": d.tipo,
                "descricao": f"{d.descricao}\n\nPrimeiro Passo: {d.primeiro_passo}\nCritério de Sucesso: {d.criterio_sucesso}",
                "impacto": None, # Could map from somewhere if IA provided impact for diretriz
                "esforco": None, # Could map from somewhere
                "prioridade": d.prioridade,
                "status": "Sugerida",
                "pre_requisitos": json.dumps(d.dependencias, ensure_ascii=False) if d.dependencias else None
            }
            diretrizes_data.append(diretriz_data)
        
        if diretrizes_data:
            diretriz_repository.bulk_create_diretrizes(db, diretrizes_data)

    return db_analise

def list_analises(db: Session, processo_id: int):
    # Validar processo
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return analise_repository.list_analises_by_processo(db, processo_id)

def get_analise(db: Session, analise_id: int):
    analise = analise_repository.get_analise_by_id(db, analise_id)
    if not analise:
        raise HTTPException(status_code=404, detail="Análise não encontrada.")
    return analise
