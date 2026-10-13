from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.alimento_region_schema import (
    AlimentoRegionCrear,
    AlimentoRegionRespuesta,
)
from services.alimento_region_service import AlimentoRegionService
from utils.auth_dependencies import get_current_user


router = APIRouter(prefix="/alimentos", tags=["Alimentos por región"])


@router.get(
    "/regionales/{municipio_divipola}",
    response_model=list[AlimentoRegionRespuesta],
)
def listar_alimentos_disponibles(
    municipio_divipola: str = Path(pattern=r"^\d{5}$"),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoRegionService(db).listar_disponibles(
        municipio_divipola
    )


@router.post(
    "/{alimento_id}/regiones",
    response_model=AlimentoRegionRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_disponibilidad(
    alimento_id: int,
    datos: AlimentoRegionCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return AlimentoRegionService(db).registrar_disponibilidad(
        alimento_id,
        datos,
        usuario_actual,
    )