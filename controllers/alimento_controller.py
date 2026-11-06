from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.alimento_schema import AlimentoActualizar, AlimentoCrear, AlimentoEstadoActualizar, AlimentoRespuesta
from services.alimento_service import AlimentoService
from utils.auth_dependencies import get_current_user


router = APIRouter(prefix="/alimentos", tags=["Alimentos"])


@router.get("/", response_model=list[AlimentoRespuesta])
def listar_alimentos(
    busqueda: str | None = Query(default=None, min_length=1),
    incluir_inactivos: bool = Query(default=False),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoService(db).listar_alimentos(busqueda, incluir_inactivos, usuario_actual)


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


@router.patch("/{alimento_id}", response_model=AlimentoRespuesta)
def actualizar_alimento(
    alimento_id: int,
    datos: AlimentoActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoService(db).actualizar_alimento(alimento_id, datos, usuario_actual)


@router.patch("/{alimento_id}/estado", response_model=AlimentoRespuesta)
def actualizar_estado_alimento(
    alimento_id: int,
    datos: AlimentoEstadoActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoService(db).actualizar_estado(alimento_id, datos.estado, usuario_actual)
