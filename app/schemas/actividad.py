from pydantic import BaseModel
from datetime import date

class ActividadCrear(BaseModel):
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool

class ActividadRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: str
    estado: str
    fecha: date
    completada: bool
    tarea_id: int