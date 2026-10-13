from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PacienteCrear(BaseModel):
    nombres: str = Field(min_length=1, max_length=100)
    apellidos: str = Field(min_length=1, max_length=100)
    fecha_nacimiento: date
    sexo: str | None = Field(default=None, max_length=20)
    municipio_divipola: str = Field(pattern=r"^\d{5}$")
    zona: Literal["URBANA", "RURAL"] | None = None
    estrato: int | None = Field(default=None, ge=1, le=6)
    presupuesto_semanal_cop: Decimal | None = Field(default=None, ge=0)

    correo: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=72)


class PacienteActualizar(BaseModel):
    nombres: str | None = Field(default=None, min_length=1, max_length=100)
    apellidos: str | None = Field(default=None, min_length=1, max_length=100)
    fecha_nacimiento: date | None = None
    sexo: str | None = Field(default=None, max_length=20)
    municipio_divipola: str | None = Field(
        default=None,
        pattern=r"^\d{5}$",
    )
    zona: Literal["URBANA", "RURAL"] | None = None
    estrato: int | None = Field(default=None, ge=1, le=6)
    presupuesto_semanal_cop: Decimal | None = Field(default=None, ge=0)
    motivo_anulacion: str | None = None


class PacienteRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nutricionista_id: int
    usuario_id: int | None
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    sexo: str | None
    municipio_divipola: str
    zona: str | None
    estrato: int | None
    presupuesto_semanal_cop: Decimal | None
    motivo_anulacion: str | None
    estado: bool
    correo: str | None