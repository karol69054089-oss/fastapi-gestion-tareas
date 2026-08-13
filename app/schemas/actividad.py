from pydantic import BaseModel, ConfigDict
from datetime import date


class ActividadCrear(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool
    tarea_id: int


class ActividadRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool
    tarea_id: int

    model_config = ConfigDict(from_attributes=True)