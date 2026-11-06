from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.usuario_schema import UsuarioCrear, UsuarioRespuesta, UsuarioEstadoActualizar, UsuarioAdminRespuesta
from services.usuario_service import UsuarioService
from utils.auth_dependencies import get_current_user


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
)


@router.get("/", response_model=list[UsuarioAdminRespuesta])
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return UsuarioService(db).listar_usuarios(usuario_actual)


@router.patch("/{usuario_id}/estado", response_model=UsuarioRespuesta)
def actualizar_estado_usuario(
    usuario_id: int,
    datos: UsuarioEstadoActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return UsuarioService(db).actualizar_estado(usuario_id, datos.estado, usuario_actual)


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
