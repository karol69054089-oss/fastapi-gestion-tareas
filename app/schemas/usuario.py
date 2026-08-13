from pydantic import BaseModel, ConfigDict


class UsuarioCrear(BaseModel):
    nombre: str
    correo: str


class UsuarioRespuesta(BaseModel):
    id: int
    nombre: str
    correo: str

    model_config = ConfigDict(from_attributes=True)