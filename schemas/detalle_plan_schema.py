from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


TipoComida = Literal[
    "DESAYUNO",
    "MEDIA_MANANA",
    "ALMUERZO",
    "MERIENDA",
    "CENA",
]


class DetallePlanCrear(BaseModel):
    dia: int = Field(ge=1, le=31)
    tipo_comida: TipoComida
    alimento_id: int | None = Field(default=None, gt=0)
    receta_id: int | None = Field(default=None, gt=0)
    cantidad: Decimal = Field(gt=0, max_digits=10, decimal_places=3)
    unidad: str = Field(min_length=1, max_length=30)

    @model_validator(mode="after")
    def validar_origen(self):
        if (self.alimento_id is None) == (self.receta_id is None):
            raise ValueError("Debes indicar un alimento o una receta, pero no ambos.")
        return self


class DetallePlanActualizar(BaseModel):
    dia: int | None = Field(default=None, ge=1, le=31)
    tipo_comida: TipoComida | None = None
    alimento_id: int | None = Field(default=None, gt=0)
    receta_id: int | None = Field(default=None, gt=0)
    cantidad: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=3,
    )
    unidad: str | None = Field(default=None, min_length=1, max_length=30)


class DetallePlanRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    version_plan_id: int
    dia: int
    tipo_comida: str
    alimento_id: int | None
    receta_id: int | None
    cantidad: Decimal
    unidad: str
    estado: bool