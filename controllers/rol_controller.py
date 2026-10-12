from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.rol_schema import RolRespuesta
from services.rol_service import RolService


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get("/", response_model=list[RolRespuesta])
def listar_roles(db: Session = Depends(get_db)):
    servicio = RolService(db)
    return servicio.listar_roles()