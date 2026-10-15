from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.usuario_schema import UsuarioCrear, UsuarioRespuesta
from services.usuario_service import UsuarioService
from utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


@router.post(
    "/bootstrap-admin",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_administrador_inicial(
    datos: UsuarioCrear,
    x_bootstrap_token: str = Header(..., alias="X-Bootstrap-Token"),
    db: Session = Depends(get_db),
):
    servicio = UsuarioService(db)
    return servicio.crear_administrador_inicial(
        datos,
        x_bootstrap_token,
    )


@router.post(
    "/nutricionistas",
    response_model=UsuarioRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_nutricionista(
    datos: UsuarioCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    servicio = UsuarioService(db)
    return servicio.crear_nutricionista(
        datos,
        usuario_actual,
    )