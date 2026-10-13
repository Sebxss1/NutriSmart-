from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AlimentoRegionCrear(BaseModel):
    municipio_divipola: str = Field(pattern=r"^\d{5}$")
    precio_cop: Decimal | None = Field(default=None, ge=0)
    disponible: bool = True
    fecha_referencia: date
    fuente: str | None = Field(default=None, max_length=200)


class AlimentoRegionRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    alimento_id: int
    municipio_divipola: str
    precio_cop: Decimal | None
    disponible: bool
    fecha_referencia: date
    fuente: str | None
    estado: bool