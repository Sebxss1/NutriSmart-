from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.consentimiento_schema import (
    ConsentimientoCrear,
    ConsentimientoRespuesta,
)
from services.consentimiento_service import ConsentimientoService
from utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/pacientes",
    tags=["Consentimientos"],
)


@router.get(
    "/{paciente_id}/consentimientos",
    response_model=list[ConsentimientoRespuesta],
)
def listar_consentimientos(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ConsentimientoService(db).listar(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/{paciente_id}/consentimientos",
    response_model=ConsentimientoRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_consentimiento(
    paciente_id: int,
    datos: ConsentimientoCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ConsentimientoService(db).crear(
        paciente_id,
        datos,
        usuario_actual,
    )


@router.delete(
    "/{paciente_id}/consentimientos/{consentimiento_id}",
    response_model=ConsentimientoRespuesta,
)
def desactivar_consentimiento(
    paciente_id: int,
    consentimiento_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ConsentimientoService(db).desactivar(
        paciente_id,
        consentimiento_id,
        usuario_actual,
    )