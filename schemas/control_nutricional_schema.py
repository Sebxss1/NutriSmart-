from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ControlNutricionalCrear(BaseModel):
    fecha_control: datetime
    peso_kg: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    estatura_cm: Decimal = Field(gt=0, max_digits=6, decimal_places=2)
    cintura_cm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=6,
        decimal_places=2,
    )
    observaciones: str | None = None


class ControlNutricionalActualizar(BaseModel):
    fecha_control: datetime | None = None
    peso_kg: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=6,
        decimal_places=2,
    )
    estatura_cm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=6,
        decimal_places=2,
    )
    cintura_cm: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=6,
        decimal_places=2,
    )
    observaciones: str | None = None


class ControlNutricionalRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    registrado_por_id: int
    fecha_control: datetime
    peso_kg: Decimal
    estatura_cm: Decimal
    cintura_cm: Decimal | None
    observaciones: str | None
    estado: bool
    creado: datetime
    actualizado: datetime