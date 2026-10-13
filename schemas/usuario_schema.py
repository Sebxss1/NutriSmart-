from pydantic import BaseModel, ConfigDict, Field


class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    correo: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=8, max_length=72)


class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    correo: str
    rol_id: int
    estado: bool