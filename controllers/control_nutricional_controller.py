from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.control_nutricional_schema import (
    ControlNutricionalActualizar,
    ControlNutricionalCrear,
    ControlNutricionalRespuesta,
)
from services.control_nutricional_service import ControlNutricionalService
from utils.auth_dependencies import get_current_user


router = APIRouter(tags=["Controles nutricionales"])


@router.get(
    "/pacientes/{paciente_id}/controles-nutricionales",
    response_model=list[ControlNutricionalRespuesta],
)
def listar_controles(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ControlNutricionalService(db).listar(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/pacientes/{paciente_id}/controles-nutricionales",
    response_model=ControlNutricionalRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_control(
    paciente_id: int,
    datos: ControlNutricionalCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ControlNutricionalService(db).crear(
        paciente_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/pacientes/{paciente_id}/controles-nutricionales/{control_id}",
    response_model=ControlNutricionalRespuesta,
)
def actualizar_control(
    paciente_id: int,
    control_id: int,
    datos: ControlNutricionalActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ControlNutricionalService(db).actualizar(
        paciente_id,
        control_id,
        datos,
        usuario_actual,
    )


@router.delete(
    "/pacientes/{paciente_id}/controles-nutricionales/{control_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def desactivar_control(
    paciente_id: int,
    control_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    ControlNutricionalService(db).desactivar(
        paciente_id,
        control_id,
        usuario_actual,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)