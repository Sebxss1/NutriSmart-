from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.modulo_schema import (
    ModuloCrear,
    ModuloRespuesta,
    ModulosRolActualizar,
)
from services.modulo_service import ModuloService
from utils.auth_dependencies import get_current_user


router = APIRouter(tags=["Módulos y accesos por rol"])


@router.get(
    "/modulos",
    response_model=list[ModuloRespuesta],
)
def listar_modulos(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ModuloService(db).listar_modulos()


@router.post(
    "/modulos",
    response_model=ModuloRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_modulo(
    datos: ModuloCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ModuloService(db).crear_modulo(datos, usuario_actual)


@router.get(
    "/roles/{rol_id}/modulos",
    response_model=list[ModuloRespuesta],
)
def listar_modulos_del_rol(
    rol_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ModuloService(db).listar_modulos_por_rol(
        rol_id,
        usuario_actual,
    )


@router.put(
    "/roles/{rol_id}/modulos",
    response_model=list[ModuloRespuesta],
)
def actualizar_modulos_del_rol(
    rol_id: int,
    datos: ModulosRolActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return ModuloService(db).actualizar_modulos_del_rol(
        rol_id,
        datos.modulo_ids,
        usuario_actual,
    )