from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.alimento_schema import AlimentoCrear, AlimentoRespuesta
from services.alimento_service import AlimentoService
from utils.auth_dependencies import get_current_user


router = APIRouter(prefix="/alimentos", tags=["Alimentos"])


@router.get("/", response_model=list[AlimentoRespuesta])
def listar_alimentos(
    busqueda: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoService(db).listar_alimentos(busqueda)


@router.post(
    "/",
    response_model=AlimentoRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_alimento(
    datos: AlimentoCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoService(db).crear_alimento(datos, usuario_actual)