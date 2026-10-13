from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.auth_repository import AuthRepository
from schemas.auth_schema import LoginRequest, TokenRespuesta
from utils.seguridad import create_access_token, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.auth_repository = AuthRepository(db)

    def login(self, datos: LoginRequest) -> TokenRespuesta:
        usuario = self.auth_repository.buscar_por_correo(datos.correo)

        if usuario is None or not verify_password(
            datos.password,
            usuario.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o contraseña incorrectos.",
            )

        if not usuario.estado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La cuenta está inactiva.",
            )

        token = create_access_token(
            {
                "sub": str(usuario.id),
                "rol_id": usuario.rol_id,
            }
        )

        return TokenRespuesta(access_token=token)