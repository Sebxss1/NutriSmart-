from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config.database import get_db
from repositories.auth_repository import AuthRepository
from utils.seguridad import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(bearer_scheme),
    ],
    db: Session = Depends(get_db),
):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(credentials.credentials)

    if not payload:
        raise unauthorized

    subject = payload.get("sub")

    if not subject or not str(subject).isdigit():
        raise unauthorized

    usuario = AuthRepository(db).buscar_por_id(int(subject))

    if not usuario or not usuario.estado:
        raise unauthorized

    return usuario