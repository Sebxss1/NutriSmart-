from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.plan_nutricional_schema import (
    PlanNutricionalCrear,
    PlanNutricionalRespuesta,
    VersionPlanCrear,
    VersionPlanEstadoActualizar,
    VersionPlanRespuesta,
)
from services.plan_nutricional_service import PlanNutricionalService
from utils.auth_dependencies import get_current_user


router = APIRouter(tags=["Planes nutricionales"])


@router.get(
    "/pacientes/{paciente_id}/planes-nutricionales",
    response_model=list[PlanNutricionalRespuesta],
)
def listar_planes(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PlanNutricionalService(db).listar_planes(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/pacientes/{paciente_id}/planes-nutricionales",
    response_model=PlanNutricionalRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_plan(
    paciente_id: int,
    datos: PlanNutricionalCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PlanNutricionalService(db).crear_plan(
        paciente_id,
        datos,
        usuario_actual,
    )


@router.get(
    "/planes-nutricionales/{plan_id}/versiones",
    response_model=list[VersionPlanRespuesta],
)
def listar_versiones(
    plan_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PlanNutricionalService(db).listar_versiones(
        plan_id,
        usuario_actual,
    )


@router.post(
    "/planes-nutricionales/{plan_id}/versiones",
    response_model=VersionPlanRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_version(
    plan_id: int,
    datos: VersionPlanCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PlanNutricionalService(db).crear_version(
        plan_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/planes-nutricionales/{plan_id}/versiones/{version_id}/estado",
    response_model=VersionPlanRespuesta,
)
def actualizar_estado_version(
    plan_id: int,
    version_id: int,
    datos: VersionPlanEstadoActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return PlanNutricionalService(db).actualizar_estado_version(
        plan_id,
        version_id,
        datos.estado_plan,
        usuario_actual,
    )