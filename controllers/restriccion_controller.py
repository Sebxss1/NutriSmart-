from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.restriccion_schema import (
    RestriccionActualizar,
    RestriccionCrear,
    RestriccionRespuesta,
)
from services.restriccion_service import RestriccionService
from utils.auth_dependencies import get_current_user


router = APIRouter(tags=["Restricciones alimentarias"])


@router.get(
    "/pacientes/{paciente_id}/restricciones-alimentarias",
    response_model=list[RestriccionRespuesta],
)
def listar_restricciones(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RestriccionService(db).listar_restricciones(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/pacientes/{paciente_id}/restricciones-alimentarias",
    response_model=RestriccionRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_restriccion(
    paciente_id: int,
    datos: RestriccionCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RestriccionService(db).crear_restriccion(
        paciente_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/pacientes/{paciente_id}/restricciones-alimentarias/{restriccion_id}",
    response_model=RestriccionRespuesta,
)
def actualizar_restriccion(
    paciente_id: int,
    restriccion_id: int,
    datos: RestriccionActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RestriccionService(db).actualizar_restriccion(
        paciente_id,
        restriccion_id,
        datos,
        usuario_actual,
    )