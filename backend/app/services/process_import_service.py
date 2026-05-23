from sqlalchemy.orm import Session
from loguru import logger
from fastapi import HTTPException
from app.models.processo import Processo
from app.models.etapa import Etapa
from app.models.conexao import Conexao
from app.services.document_reader_service import DocumentReaderService
from app.services.document_sanitizer_service import DocumentSanitizerService
from app.services.process_import_ia_service import ProcessImportIAService
from app.schemas.importacao_processo_schema import ProcessImportResponseSchema
from datetime import datetime

class ProcessImportService:
    @staticmethod
    def import_process_from_docx(db: Session, file_bytes: bytes, filename: str) -> ProcessImportResponseSchema:
        """
        Orquestra a importação de processo por DOCX:
        1. Leitura documental.
        2. Sanitização de credenciais.
        3. Chamada ao motor de IA para estruturar as entidades.
        4. Gravação transacional em banco de dados SQLite com rollback automático em falhas.
        """
        logger.info(f"Orquestrador: Iniciando fluxo de importação para o arquivo '{filename}'.")
        
        # 1. Leitura do arquivo DOCX
        doc_result = DocumentReaderService.read_docx(file_bytes, filename)
        doc_metadata = doc_result.to_dict()["metadata"]
        
        # 2. Sanitização de credenciais
        sanitized_doc = DocumentSanitizerService.sanitize(doc_result.text)
        
        # 3. Chamada à Inteligência Artificial
        ai_result = ProcessImportIAService.call_import_ia(sanitized_doc.text, doc_metadata)
        
        # Unificar alertas sensíveis (tanto os locais do sanitizador regex quanto os identificados pela IA)
        all_sensitive_alerts = []
        seen_alerts = set()
        
        # Adicionar alertas do sanitizador
        for alert in sanitized_doc.alerts:
            desc_hash = alert["descricao"]
            if desc_hash not in seen_alerts:
                seen_alerts.add(desc_hash)
                all_sensitive_alerts.append(alert)
                
        # Adicionar alertas identificados pela IA
        for alert in ai_result.alertas_sensiveis:
            desc_hash = alert.descricao
            if desc_hash not in seen_alerts:
                seen_alerts.add(desc_hash)
                all_sensitive_alerts.append({
                    "tipo": alert.tipo.value,
                    "descricao": alert.descricao,
                    "acao_aplicada": alert.acao_aplicada.value
                })

        # 4. Persistência Transacional no Banco de Dados
        try:
            logger.info("Orquestrador: Iniciando persistência transacional.")
            
            # Criar processo
            processo_data = ai_result.processo
            
            # Gerar texto de observações enriquecido com as lacunas identificadas
            observacoes_com_lacunas = processo_data.observacoes or ""
            if ai_result.lacunas_mapeamento:
                observacoes_com_lacunas += "\n\n=== LACUNAS DE MAPEAMENTO DETECTADAS POR IA ===\n"
                for idx, gap in enumerate(ai_result.lacunas_mapeamento, 1):
                    observacoes_com_lacunas += f"{idx}. [{gap.campo_ou_tema}]: {gap.descricao} -> Recomendado: {gap.pergunta_recommended if hasattr(gap, 'pergunta_recommended') else gap.pergunta_recomendada}\n"
            
            if all_sensitive_alerts:
                observacoes_com_lacunas += "\n\n=== ALERTAS DE SEGURANÇA E HIGIENIZAÇÃO ===\n"
                for idx, alert in enumerate(all_sensitive_alerts, 1):
                    observacoes_com_lacunas += f"{idx}. [{alert['tipo'].upper()}] - {alert['descricao']} (Ação: {alert['acao_aplicada']})\n"

            db_processo = Processo(
                nome=processo_data.nome,
                area=processo_data.area,
                descricao=processo_data.descricao,
                objetivo=processo_data.objetivo,
                responsavel=processo_data.responsavel,
                periodicidade=processo_data.periodicidade,
                criticidade=processo_data.criticidade,
                status=processo_data.status or "Ativo",
                sistemas_utilizados=processo_data.sistemas_utilizados,
                documentos_utilizados=processo_data.documentos_utilizados,
                observacoes=observacoes_com_lacunas,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.add(db_processo)
            db.flush()  # Gera o ID do processo no SQLite
            processo_id = db_processo.id
            logger.info(f"Orquestrador: Processo cadastrado com ID temporário {processo_id}.")

            # Criar etapas e calcular posições X/Y
            mapa_etapas_ids = {}  # mapa: ordem -> id de banco
            etapas_criadas_count = 0
            
            # Organizar etapas ordenando pela sequência indicada
            etapas_ordenadas = sorted(ai_result.etapas, key=lambda x: x.ordem)
            
            # Dicionário auxiliar para sabermos se uma etapa é destino de alguma transição condicional/falha
            etapas_destino_desvio = set()
            for conn in ai_result.conexoes:
                if conn.tipo_conexao.value in ["condicional", "falha"]:
                    etapas_destino_desvio.add(conn.ordem_destino)

            for etapa in etapas_ordenadas:
                # Layout inteligente: Disposição linear horizontal (esquerda para direita)
                # Cada nó tem 300px de espaçamento horizontal.
                posicao_x = 100.0 + (etapa.ordem - 1) * 300.0
                
                # Se for uma etapa que representa um desvio lógico (condicional/falha),
                # posiciona um pouco abaixo (+150px) para não sobrepor na linha principal horizontal.
                if etapa.ordem in etapas_destino_desvio or etapa.tipo_etapa.value == "Decisão":
                    posicao_y = 350.0
                else:
                    posicao_y = 200.0

                db_etapa = Etapa(
                    processo_id=processo_id,
                    nome=etapa.nome,
                    descricao=etapa.descricao,
                    responsavel=etapa.responsavel,
                    entrada=etapa.entrada,
                    saida=etapa.saida,
                    sistema_utilizado=etapa.sistema_utilizado,
                    tempo_estimado=etapa.tempo_estimado,
                    tipo_etapa=etapa.tipo_etapa.value,
                    risco=etapa.risco,
                    gargalo=etapa.gargalo,
                    oportunidade_automacao=etapa.oportunidade_automacao,
                    posicao_x=posicao_x,
                    posicao_y=posicao_y,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.add(db_etapa)
                db.flush()  # Gera o ID da etapa
                mapa_etapas_ids[etapa.ordem] = db_etapa.id
                etapas_criadas_count += 1

            logger.info(f"Orquestrador: {etapas_criadas_count} etapas criadas temporariamente.")

            # Criar Conexões
            conexoes_criadas_count = 0
            
            # Se a IA não retornou conexões explícitas, nós criamos o sequenciamento padrão linear
            conexoes_para_criar = []
            if not ai_result.conexoes:
                logger.info("Orquestrador: IA não retornou conexões. Gerando sequenciamento linear padrão.")
                for i in range(len(etapas_ordenadas) - 1):
                    origem = etapas_ordenadas[i].ordem
                    destino = etapas_ordenadas[i+1].ordem
                    conexoes_para_criar.append({
                        "ordem_origem": origem,
                        "ordem_destino": destino,
                        "tipo_conexao": "padrao",
                        "condicao": None
                    })
            else:
                for conn in ai_result.conexoes:
                    conexoes_para_criar.append({
                        "ordem_origem": conn.ordem_origem,
                        "ordem_destino": conn.ordem_destino,
                        "tipo_conexao": conn.tipo_conexao.value,
                        "condicao": conn.condicao
                    })

            for conn in conexoes_para_criar:
                origem_id = mapa_etapas_ids.get(conn["ordem_origem"])
                destino_id = mapa_etapas_ids.get(conn["ordem_destino"])
                
                # Só cadastrar se ambas as etapas existirem no nosso mapa de ordem
                if origem_id and destino_id:
                    db_conexao = Conexao(
                        processo_id=processo_id,
                        etapa_origem_id=origem_id,
                        etapa_destino_id=destino_id,
                        tipo_conexao=conn["tipo_conexao"],
                        condicao=conn["condicao"],
                        created_at=datetime.utcnow()
                    )
                    db.add(db_conexao)
                    conexoes_criadas_count += 1
                else:
                    logger.warning(f"Orquestrador: Falha ao ligar etapas. Ordem de origem {conn['ordem_origem']} ou destino {conn['ordem_destino']} não encontrada.")

            logger.info(f"Orquestrador: {conexoes_criadas_count} conexões lógicas criadas temporariamente.")

            # 5. Commit final da transação atômica (grava tudo ou nada)
            db.commit()
            logger.info(f"Orquestrador: Transação confirmada no SQLite. Processo {processo_id} gravado com absoluto sucesso.")

            # Resumo textual das lacunas para o response
            resumo_lacunas = []
            for gap in ai_result.lacunas_mapeamento:
                resumo_lacunas.append(f"{gap.campo_ou_tema}: {gap.descricao}")

            return ProcessImportResponseSchema(
                processo_id=processo_id,
                mensagem="Processo importado com sucesso. Revise as lacunas e dados antes de executar o diagnóstico de IA.",
                nome_processo=processo_data.nome,
                etapas_criadas=etapas_criadas_count,
                conexoes_criadas=conexoes_criadas_count,
                lacunas_identificadas=resumo_lacunas,
                alertas_sensiveis=[
                    {
                        "tipo": alert["tipo"],
                        "descricao": alert["descricao"],
                        "acao_aplicada": alert["acao_aplicada"]
                    } for alert in all_sensitive_alerts
                ]
            )

        except Exception as e:
            # Qualquer falha dispara o Rollback completo (mantém integridade de dados)
            db.rollback()
            logger.error(f"Orquestrador: Ocorreu um erro no processo de gravação. Rollback executado. Detalhes: {e}")
            raise HTTPException(
                status_code=500,
                detail="Erro interno de banco de dados ao salvar o processo importado. A transação foi desfeita."
            )
