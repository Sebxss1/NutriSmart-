from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.paciente_schema import (
    PacienteActualizar,
    PacienteCrear,
    PacienteRespuesta,
)
from services.paciente_service import PacienteService
from utils.auth_dependencies import get_current_user

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get(
    "/",
    response_model=list[PacienteRespuesta],
)
def listar_pacientes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PacienteService(db).listar_pacientes(usuario_actual)


@router.get(
    "/mi-perfil",
    response_model=PacienteRespuesta,
)
def obtener_mi_perfil(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PacienteService(db).obtener_perfil_propio(usuario_actual)


@router.get(
    "/{paciente_id}",
    response_model=PacienteRespuesta,
)
def obtener_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PacienteService(db).obtener_paciente(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/",
    response_model=PacienteRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_paciente(
    datos: PacienteCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PacienteService(db).crear_paciente(
        datos,
        usuario_actual,
    )


@router.patch(
    "/{paciente_id}",
    response_model=PacienteRespuesta,
)
def actualizar_paciente(
    paciente_id: int,
    datos: PacienteActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PacienteService(db).actualizar_paciente(
        paciente_id,
        datos,
        usuario_actual,
    )
