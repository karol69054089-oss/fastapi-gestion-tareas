from pydantic import BaseModel, ConfigDict
from datetime import date
from app.schemas.usuario import UsuarioRespuesta


class TareaCrear(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    avance: float
    fecha_inicio: date
    fecha_final: date
    usuario_id: int


class TareaRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    avance: float
    fecha_inicio: date
    fecha_final: date
    usuario_id: int
    usuario: UsuarioRespuesta | None = None  # Muestra el usuario asociado

    model_config = ConfigDict(from_attributes=True)