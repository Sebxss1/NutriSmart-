from datetime import datetime

from pydantic import BaseModel, ConfigDict

class RolRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nombre: str
    descripcion: str | None
    estado: bool
    creado: datetime
    actualizado: datetime
    