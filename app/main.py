from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Base de datos y modelos
from app.database import engine, get_db
from app.models import Base, UsuarioModel, TareaModel, ActividadModel

# Esquemas Pydantic
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta
from app.schemas.tarea import TareaCrear, TareaRespuesta
from app.schemas.actividad import ActividadCrear, ActividadRespuesta


# =========================================================
# CREACIÓN DE TABLAS
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# CONFIGURACIÓN DE LA API
# =========================================================

app = FastAPI(
    title="API de Gestión de Tareas",
    description="Proyecto ADSO - FastAPI con SQLAlchemy y PostgreSQL",
    version="1.0.0"
)


# =========================================================
# ENDPOINT PRINCIPAL
# =========================================================

@app.get("/")
def leer_raiz():
    return {
        "mensaje": "Bienvenido a la API de Gestión de Tareas - SENA ADSO"
    }


# =========================================================
# USUARIOS - CREAR
# =========================================================

@app.post(
    "/usuarios/",
    response_model=UsuarioRespuesta,
    status_code=201
)
def crear_usuario(
    usuario: UsuarioCrear,
    db: Session = Depends(get_db)
):
    # Verificar que el correo sea único
    usuario_existente = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.correo == usuario.correo)
        .first()
    )

    if usuario_existente:
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado"
        )

    db_usuario = UsuarioModel(
        nombre=usuario.nombre,
        correo=usuario.correo
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)

    return db_usuario


# =========================================================
# USUARIOS - LEER
# =========================================================

@app.get(
    "/usuarios/",
    response_model=List[UsuarioRespuesta]
)
def listar_usuarios(
    db: Session = Depends(get_db)
):
    usuarios = db.query(UsuarioModel).all()

    return usuarios


# =========================================================
# USUARIOS - EDITAR
# =========================================================

@app.patch(
    "/usuarios/{usuario_id}",
    response_model=UsuarioRespuesta
)
def actualizar_usuario(
    usuario_id: int,
    usuario: UsuarioCrear,
    db: Session = Depends(get_db)
):
    db_usuario = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.id == usuario_id)
        .first()
    )

    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Verificar que el nuevo correo no esté
    # siendo utilizado por otro usuario
    correo_existente = (
        db.query(UsuarioModel)
        .filter(
            UsuarioModel.correo == usuario.correo,
            UsuarioModel.id != usuario_id
        )
        .first()
    )

    if correo_existente:
        raise HTTPException(
            status_code=409,
            detail="El correo ya está registrado"
        )

    db_usuario.nombre = usuario.nombre
    db_usuario.correo = usuario.correo

    db.commit()
    db.refresh(db_usuario)

    return db_usuario


# =========================================================
# USUARIOS - ELIMINAR
# =========================================================

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    db_usuario = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.id == usuario_id)
        .first()
    )

    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(db_usuario)
    db.commit()

    return {
        "mensaje": "Usuario eliminado con éxito"
    }


# =========================================================
# TAREAS - CREAR
# =========================================================

@app.post(
    "/tareas/",
    response_model=TareaRespuesta,
    status_code=201
)
def crear_tarea(
    tarea: TareaCrear,
    db: Session = Depends(get_db)
):
    # Validar que el usuario exista
    usuario = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.id == tarea.usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario asignado no existe"
        )

    db_tarea = TareaModel(
        nombre=tarea.nombre,
        descripcion=tarea.descripcion,
        estado=tarea.estado,
        avance=tarea.avance,
        fecha_inicio=tarea.fecha_inicio,
        fecha_final=tarea.fecha_final,
        usuario_id=tarea.usuario_id
    )

    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)

    return db_tarea


# =========================================================
# TAREAS - LEER
# =========================================================

@app.get(
    "/tareas/",
    response_model=List[TareaRespuesta]
)
def listar_tareas(
    db: Session = Depends(get_db)
):
    tareas = db.query(TareaModel).all()

    return tareas


# =========================================================
# TAREAS - EDITAR
# =========================================================

@app.patch(
    "/tareas/{tarea_id}",
    response_model=TareaRespuesta
)
def actualizar_tarea(
    tarea_id: int,
    tarea: TareaCrear,
    db: Session = Depends(get_db)
):
    db_tarea = (
        db.query(TareaModel)
        .filter(TareaModel.id == tarea_id)
        .first()
    )

    if not db_tarea:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    # Validar que el usuario exista
    usuario = (
        db.query(UsuarioModel)
        .filter(UsuarioModel.id == tarea.usuario_id)
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario asignado no existe"
        )

    db_tarea.nombre = tarea.nombre
    db_tarea.descripcion = tarea.descripcion
    db_tarea.estado = tarea.estado
    db_tarea.avance = tarea.avance
    db_tarea.fecha_inicio = tarea.fecha_inicio
    db_tarea.fecha_final = tarea.fecha_final
    db_tarea.usuario_id = tarea.usuario_id

    db.commit()
    db.refresh(db_tarea)

    return db_tarea


# =========================================================
# TAREAS - ELIMINAR
# =========================================================

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(
    tarea_id: int,
    db: Session = Depends(get_db)
):
    db_tarea = (
        db.query(TareaModel)
        .filter(TareaModel.id == tarea_id)
        .first()
    )

    if not db_tarea:
        raise HTTPException(
            status_code=404,
            detail="Tarea no encontrada"
        )

    db.delete(db_tarea)
    db.commit()

    return {
        "mensaje": "Tarea eliminada con éxito"
    }


# =========================================================
# ACTIVIDADES - CREAR
# =========================================================

@app.post(
    "/tareas/{tarea_id}/actividades/",
    response_model=ActividadRespuesta,
    status_code=201
)
def crear_actividad(
    tarea_id: int,
    actividad: ActividadCrear,
    db: Session = Depends(get_db)
):
    # Validar que la tarea exista
    tarea = (
        db.query(TareaModel)
        .filter(TareaModel.id == tarea_id)
        .first()
    )

    if not tarea:
        raise HTTPException(
            status_code=404,
            detail="La tarea asignada no existe"
        )

    # Verificar que el tarea_id del cuerpo
    # coincida con el de la URL
    if actividad.tarea_id != tarea_id:
        raise HTTPException(
            status_code=400,
            detail="El tarea_id debe coincidir con el de la URL"
        )

    db_actividad = ActividadModel(
        nombre=actividad.nombre,
        descripcion=actividad.descripcion,
        estado=actividad.estado,
        fecha=actividad.fecha,
        completada=actividad.completada,
        tarea_id=tarea_id
    )

    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)

    return db_actividad


# =========================================================
# ACTIVIDADES - LEER
# =========================================================

@app.get(
    "/actividades/",
    response_model=List[ActividadRespuesta]
)
def listar_actividades(
    db: Session = Depends(get_db)
):
    actividades = db.query(ActividadModel).all()

    return actividades


# =========================================================
# ACTIVIDADES - EDITAR
# =========================================================

@app.patch(
    "/actividades/{actividad_id}",
    response_model=ActividadRespuesta
)
def actualizar_actividad(
    actividad_id: int,
    actividad: ActividadCrear,
    db: Session = Depends(get_db)
):
    db_actividad = (
        db.query(ActividadModel)
        .filter(ActividadModel.id == actividad_id)
        .first()
    )

    if not db_actividad:
        raise HTTPException(
            status_code=404,
            detail="Actividad no encontrada"
        )

    # Validar que la tarea exista
    tarea = (
        db.query(TareaModel)
        .filter(TareaModel.id == actividad.tarea_id)
        .first()
    )

    if not tarea:
        raise HTTPException(
            status_code=404,
            detail="La tarea asignada no existe"
        )

    db_actividad.nombre = actividad.nombre
    db_actividad.descripcion = actividad.descripcion
    db_actividad.estado = actividad.estado
    db_actividad.fecha = actividad.fecha
    db_actividad.completada = actividad.completada
    db_actividad.tarea_id = actividad.tarea_id

    db.commit()
    db.refresh(db_actividad)

    return db_actividad


# =========================================================
# ACTIVIDADES - ELIMINAR
# =========================================================

@app.delete("/actividades/{actividad_id}")
def eliminar_actividad(
    actividad_id: int,
    db: Session = Depends(get_db)
):
    db_actividad = (
        db.query(ActividadModel)
        .filter(ActividadModel.id == actividad_id)
        .first()
    )

    if not db_actividad:
        raise HTTPException(
            status_code=404,
            detail="Actividad no encontrada"
        )

    db.delete(db_actividad)
    db.commit()

    return {
        "mensaje": "Actividad eliminada con éxito"
    }