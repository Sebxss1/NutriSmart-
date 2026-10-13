from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from repositories.auth_repository import AuthRepository
from schemas.auth_schema import LoginRequest, Token
from utils.auth_dependencies import get_current_user
from utils.seguridad import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def iniciar_sesion(
    datos: LoginRequest,
    db: Session = Depends(get_db),
):
    usuario = AuthRepository(db).buscar_por_correo(datos.correo)

    if not usuario or not verify_password(
        datos.password,
        usuario.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )

    if not usuario.estado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está desactivado",
        )

    token = create_access_token(
        {
            "sub": str(usuario.id),
            "rol_id": usuario.rol_id,
        }
    )

    return Token(access_token=token)


@router.get("/me")
def ver_usuario_actual(
    usuario=Depends(get_current_user),
):
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "rol_id": usuario.rol_id,
    }