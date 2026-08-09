from pydantic import BaseModel


class UsuarioCrear(BaseModel):
    nombre: str
    correo: str


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: str