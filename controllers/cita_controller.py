from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.cita_schema import (
    CitaActualizar,
    CitaCrear,
    CitaEstadoActualizar,
    CitaRespuesta,
)
from services.cita_service import CitaService
from utils.auth_dependencies import get_current_user


router = APIRouter(tags=["Citas"])


@router.get(
    "/pacientes/{paciente_id}/citas",
    response_model=list[CitaRespuesta],
)
def listar_citas(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CitaService(db).listar(paciente_id, usuario_actual)


@router.post(
    "/pacientes/{paciente_id}/citas",
    response_model=CitaRespuesta,
    status_code=201,
)
def crear_cita(
    paciente_id: int,
    datos: CitaCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CitaService(db).crear(
        paciente_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/pacientes/{paciente_id}/citas/{cita_id}",
    response_model=CitaRespuesta,
)
def reprogramar_cita(
    paciente_id: int,
    cita_id: int,
    datos: CitaActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CitaService(db).reprogramar(
        paciente_id,
        cita_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/pacientes/{paciente_id}/citas/{cita_id}/estado",
    response_model=CitaRespuesta,
)
def cambiar_estado_cita(
    paciente_id: int,
    cita_id: int,
    datos: CitaEstadoActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CitaService(db).cambiar_estado(
        paciente_id,
        cita_id,
        datos.estado_cita,
        usuario_actual,
    )