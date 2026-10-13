from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


TipoComida = Literal[
    "DESAYUNO",
    "MEDIA_MANANA",
    "ALMUERZO",
    "MERIENDA",
    "CENA",
]


class RecetaCrear(BaseModel):
    codigo: str = Field(min_length=1, max_length=60)
    nombre: str = Field(min_length=1, max_length=160)
    tipo_comida: TipoComida
    instrucciones: str | None = None


class RecetaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    tipo_comida: str
    instrucciones: str | None
    estado: bool


class IngredienteRecetaCrear(BaseModel):
    alimento_id: int = Field(gt=0)
    cantidad: Decimal = Field(gt=0)
    unidad: str = Field(min_length=1, max_length=30)


class IngredienteRecetaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    receta_id: int
    alimento_id: int
    cantidad: Decimal
    unidad: str
    estado: bool
    
    
class RecetaActualizar(BaseModel):
    codigo: str | None = Field(default=None, min_length=1, max_length=60)
    nombre: str | None = Field(default=None, min_length=1, max_length=160)
    tipo_comida: TipoComida | None = None
    instrucciones: str | None = None


class IngredienteRecetaActualizar(BaseModel):
    cantidad: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=3,
    )
    unidad: str | None = Field(default=None, min_length=1, max_length=30)