from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.detalle_plan_schema import (
    DetallePlanActualizar,
    DetallePlanCrear,
    DetallePlanRespuesta,
)
from services.detalle_plan_service import DetallePlanService
from utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/versiones-plan",
    tags=["Detalle de planes"],
)


@router.get(
    "/{version_id}/detalles",
    response_model=list[DetallePlanRespuesta],
)
def listar_detalles(
    version_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return DetallePlanService(db).listar_detalles(
        version_id,
        usuario_actual,
    )


@router.post(
    "/{version_id}/detalles",
    response_model=DetallePlanRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_detalle(
    version_id: int,
    datos: DetallePlanCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return DetallePlanService(db).crear_detalle(
        version_id,
        datos,
        usuario_actual,
    )


@router.patch(
    "/{version_id}/detalles/{detalle_id}",
    response_model=DetallePlanRespuesta,
)
def actualizar_detalle(
    version_id: int,
    detalle_id: int,
    datos: DetallePlanActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return DetallePlanService(db).actualizar_detalle(
        version_id,
        detalle_id,
        datos,
        usuario_actual,
    )


@router.delete(
    "/{version_id}/detalles/{detalle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_detalle(
    version_id: int,
    detalle_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    DetallePlanService(db).eliminar_detalle(
        version_id,
        detalle_id,
        usuario_actual,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)