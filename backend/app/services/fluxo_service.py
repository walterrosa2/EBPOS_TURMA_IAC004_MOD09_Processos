from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services import processo_service
from app.repositories import etapa_repository, conexao_repository
from app.schemas.fluxo_schema import FluxoResponse

def obter_fluxo(db: Session, processo_id: int) -> dict:
    # Verify process exists
    processo_service.obter_processo(db, processo_id)
    
    etapas = etapa_repository.list_etapas_by_processo(db, processo_id)
    conexoes = conexao_repository.list_conexoes_by_processo(db, processo_id)
    
    return {
        "etapas": etapas,
        "conexoes": conexoes
    }

def salvar_fluxo(db: Session, processo_id: int, payload: dict) -> dict:
    # Verify process exists
    processo_service.obter_processo(db, processo_id)
    
    payload_etapas = payload.get("etapas", [])
    payload_conexoes = payload.get("conexoes", [])
    
    # 2. Validar se todas as etapas do payload pertencem ao processo
    etapa_ids = [e["id"] for e in payload_etapas if "id" in e]
    if etapa_ids:
        etapas_db = etapa_repository.list_etapas_by_ids(db, etapa_ids)
        if len(etapas_db) != len(etapa_ids):
             raise HTTPException(status_code=400, detail="Uma ou mais etapas não encontradas.")
        
        for etapa_db in etapas_db:
            if etapa_db.processo_id != processo_id:
                raise HTTPException(status_code=400, detail="Uma ou mais etapas pertencem a outro processo.")
                
            # 3. Atualizar posições X/Y das etapas informadas
            for e_payload in payload_etapas:
                if e_payload["id"] == etapa_db.id:
                    etapa_repository.update_etapa_position(
                        db, etapa_db, e_payload.get("posicao_x"), e_payload.get("posicao_y")
                    )
    
    # 4. Validar se todas as conexões ligam etapas do mesmo processo
    todas_etapas_processo = etapa_repository.list_etapas_by_processo(db, processo_id)
    etapas_processo_ids = {e.id for e in todas_etapas_processo}
    
    for c in payload_conexoes:
        if c["etapa_origem_id"] not in etapas_processo_ids or c["etapa_destino_id"] not in etapas_processo_ids:
            raise HTTPException(status_code=400, detail="Conexão inválida: as etapas devem pertencer ao mesmo processo.")
    
    # 5. Substituir conexões atuais do processo pelas conexões recebidas.
    conexao_repository.delete_conexoes_by_processo(db, processo_id)
    for c in payload_conexoes:
        conexao_repository.create_conexao(db, processo_id, c)
        
    # 6. Retornar fluxo completo atualizado.
    return obter_fluxo(db, processo_id)
