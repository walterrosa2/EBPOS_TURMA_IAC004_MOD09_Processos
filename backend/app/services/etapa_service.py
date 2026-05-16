from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import etapa_repository, conexao_repository
from app.services import processo_service
from app.schemas.etapa_schema import EtapaCreate
from app.models.etapa import Etapa

def listar_etapas(db: Session, processo_id: int) -> List[Etapa]:
    # Validate process exists
    processo_service.obter_processo(db, processo_id)
    return etapa_repository.list_etapas_by_processo(db, processo_id)

def obter_etapa(db: Session, etapa_id: int) -> Etapa:
    etapa = etapa_repository.get_etapa_by_id(db, etapa_id)
    if not etapa:
        raise HTTPException(status_code=404, detail="Etapa não encontrada.")
    return etapa

def criar_etapa(db: Session, processo_id: int, payload: EtapaCreate) -> Etapa:
    # Validate process exists
    processo_service.obter_processo(db, processo_id)
    return etapa_repository.create_etapa(db, processo_id, payload)

def atualizar_etapa(db: Session, etapa_id: int, payload: EtapaCreate) -> Etapa:
    etapa = obter_etapa(db, etapa_id)
    return etapa_repository.update_etapa(db, etapa, payload.model_dump(exclude_unset=True))

def excluir_etapa(db: Session, etapa_id: int) -> None:
    etapa = obter_etapa(db, etapa_id)
    # Excluir conexões orfãs
    conexao_repository.delete_conexoes_by_etapa(db, etapa_id)
    etapa_repository.delete_etapa(db, etapa)
