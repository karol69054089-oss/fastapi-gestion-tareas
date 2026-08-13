from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importaciones de tu base de datos y modelos
from app.database import engine, get_db
from app.models import Base, UsuarioModel, TareaModel, ActividadModel

# Importaciones de tus esquemas actualizados
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta
from app.schemas.tarea import TareaCrear, TareaRespuesta
from app.schemas.actividad import ActividadCrear, ActividadRespuesta

# Crea las tablas en PostgreSQL automáticamente al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión de Tareas",
    description="Proyecto ADSO - FastAPI con SQLAlchemy y PostgreSQL",
    version="1.0.0"
)


@app.get("/")
def leer_raiz():
    return {"mensaje": "Bienvenido a la API de Gestión de Tareas - SENA ADSO"}


# ==========================================
# ENDPOINTS DE USUARIOS
# ==========================================

@app.post("/usuarios/", response_model=UsuarioRespuesta, status_code=201)
def crear_usuario(usuario: UsuarioCrear, db: Session = Depends(get_db)):
    db_usuario = UsuarioModel(nombre=usuario.nombre, correo=usuario.correo)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@app.get("/usuarios/", response_model=List[UsuarioRespuesta])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioModel).all()
    return usuarios


# ==========================================
# ENDPOINTS DE TAREAS
# ==========================================

@app.post("/tareas/", response_model=TareaRespuesta, status_code=201)
def crear_tarea(tarea: TareaCrear, db: Session = Depends(get_db)):
    # Validar que el usuario exista antes de crear la tarea
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == tarea.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario asignado no existe")

    db_tarea = TareaModel(**tarea.model_dump())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea


@app.get("/tareas/", response_model=List[TareaRespuesta])
def listar_tareas(db: Session = Depends(get_db)):
    tareas = db.query(TareaModel).all()
    return tareas


# ==========================================
# ENDPOINTS DE ACTIVIDADES
# ==========================================

@app.post("/actividades/", response_model=ActividadRespuesta, status_code=201)
def crear_actividad(actividad: ActividadCrear, db: Session = Depends(get_db)):
    # Validar que la tarea exista
    tarea = db.query(TareaModel).filter(TareaModel.id == actividad.tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="La tarea asignada no existe")

    db_actividad = ActividadModel(**actividad.model_dump())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad


@app.get("/actividades/", response_model=List[ActividadRespuesta])
def listar_actividades(db: Session = Depends(get_db)):
    actividades = db.query(ActividadModel).all()
    return actividades

# ==========================================
# ENDPOINTS DE EDICIÓN (PUT) Y ELIMINACIÓN (DELETE)
# ==========================================

# Ejemplo: Cambiar estado de completada en actividad
@app.patch("/actividades/{actividad_id}", response_model=ActividadRespuesta)
def actualizar_actividad(actividad_id: int, db: Session = Depends(get_db)):
    db_actividad = db.query(ActividadModel).filter(ActividadModel.id == actividad_id).first()
    if not db_actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    # Cambia True por False o viceversa
    db_actividad.completada = not db_actividad.completada
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

# Ejemplo: Eliminar una tarea
@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = db.query(TareaModel).filter(TareaModel.id == tarea_id).first()
    if not db_tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(db_tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada con éxito"}