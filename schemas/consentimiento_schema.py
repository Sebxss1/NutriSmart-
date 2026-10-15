from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ConsentimientoCrear(BaseModel):
    version_texto: str = Field(min_length=1, max_length=40)
    fecha_aceptacion: datetime
    otorgado_por: str = Field(min_length=1, max_length=160)
    tipo_otorgante: Literal["PACIENTE", "REPRESENTANTE"]


class ConsentimientoRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    version_texto: str
    fecha_aceptacion: datetime
    otorgado_por: str
    tipo_otorgante: str
    registrado_por_id: int
    estado: bool
    creado: datetime
    actualizado: datetime