from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AlimentoCrear(BaseModel):
    codigo: str = Field(min_length=1, max_length=60)
    nombre: str = Field(min_length=1, max_length=160)
    categoria: str = Field(min_length=1, max_length=80)
    unidad_base: str = Field(default="100 g", max_length=30)

    energia_kcal: Decimal | None = Field(default=None, ge=0)
    proteina_g: Decimal | None = Field(default=None, ge=0)
    carbohidratos_g: Decimal | None = Field(default=None, ge=0)
    grasa_g: Decimal | None = Field(default=None, ge=0)
    fibra_g: Decimal | None = Field(default=None, ge=0)
    sodio_mg: Decimal | None = Field(default=None, ge=0)

    fuente_dato: str | None = Field(
        default="ICBF - TCAC 2018",
        max_length=200,
    )


class AlimentoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    categoria: str
    unidad_base: str
    energia_kcal: Decimal | None
    proteina_g: Decimal | None
    carbohidratos_g: Decimal | None
    grasa_g: Decimal | None
    fibra_g: Decimal | None
    sodio_mg: Decimal | None
    fuente_dato: str | None
    estado: bool