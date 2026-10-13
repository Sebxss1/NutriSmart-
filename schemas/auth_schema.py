from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    correo: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=72)
    
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
class UsuarioAutenticado(BaseModel):
    id: int
    nombre: str
    correo: str
    rol_id: int