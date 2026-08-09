from pydantic import BaseModel
from datetime import date


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