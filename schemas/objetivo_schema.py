from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class ObjetivoCrear(BaseModel):
    tipo: str = Field(min_length=1, max_length=60)
    descripcion: str | None = None
    meta_cuantificable: str | None = Field(default=None, max_length=200)
    fecha_inicio: date | None = None


class ObjetivoActualizar(BaseModel):
    tipo: str | None = Field(default=None, min_length=1, max_length=60)
    descripcion: str | None = None
    meta_cuantificable: str | None = Field(default=None, max_length=200)
    fecha_inicio: date | None = None
    estado: bool | None = None


class ObjetivoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    tipo: str
    descripcion: str | None
    meta_cuantificable: str | None
    fecha_inicio: date
    estado: bool