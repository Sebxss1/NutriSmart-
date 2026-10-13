from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.objetivo_schema import (
    ObjetivoActualizar,
    ObjetivoCrear,
    ObjetivoRespuesta,
)
from services.objetivo_service import ObjetivoService
from utils.auth_dependencies import get_current_user


router = APIRouter(tags=["Objetivos nutricionales"])


@router.get(
    "/pacientes/{paciente_id}/objetivos-nutricionales",
    response_model=list[ObjetivoRespuesta],
)
def listar_objetivos(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ObjetivoService(db).listar_objetivos(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/pacientes/{paciente_id}/objetivos-nutricionales",
    response_model=ObjetivoRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_objetivo(
    paciente_id: int,
    datos: ObjetivoCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ObjetivoService(db).crear_objetivo(
        paciente_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/pacientes/{paciente_id}/objetivos-nutricionales/{objetivo_id}",
    response_model=ObjetivoRespuesta,
)
def actualizar_objetivo(
    paciente_id: int,
    objetivo_id: int,
    datos: ObjetivoActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ObjetivoService(db).actualizar_objetivo(
        paciente_id,
        objetivo_id,
        datos,
        usuario_actual,
    )