from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class CondicionMedicaCrear(BaseModel):
    codigo: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = None


class CondicionMedicaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    descripcion: str | None
    estado: bool


class PacienteCondicionCrear(BaseModel):
    condicion_id: int
    observaciones: str | None = None


class PacienteCondicionRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    condicion_id: int
    observaciones: str | None
    fecha_registro: date
    estado: bool