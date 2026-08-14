from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.database import engine, get_db
from app.models import Base, UsuarioModel, TareaModel, ActividadModel

from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta
from app.schemas.tarea import TareaCrear, TareaRespuesta
from app.schemas.actividad import ActividadCrear, ActividadRespuesta


# Crear las tablas en PostgreSQL
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API de Gestión de Tareas",
    description="Proyecto ADSO - FastAPI con SQLAlchemy y PostgreSQL",
    version="1.0.0"
)


# =========================================================
# INICIO
# =========================================================

@app.get("/")
def leer_raiz():
    return {
        "mensaje": "Bienvenido a la API de Gestión de Tareas - SENA ADSO"
    }


# =========================================================
# USUARIOS - CRUD
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
    # Verificar que el correo no exista
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


@app.get(
    "/usuarios/",
    response_model=List[UsuarioRespuesta]
)
def listar_usuarios(
    db: Session = Depends(get_db)
):
    return db.query(UsuarioModel).all()


@app.put(
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
            detail="El correo ya está registrado por otro usuario"
        )

    db_usuario.nombre = usuario.nombre
    db_usuario.correo = usuario.correo

    db.commit()
    db.refresh(db_usuario)

    return db_usuario


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
# TAREAS - CRUD
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
        **tarea.model_dump()
    )

    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)

    return db_tarea


@app.get(
    "/tareas/",
    response_model=List[TareaRespuesta]
)
def listar_tareas(
    db: Session = Depends(get_db)
):
    return db.query(TareaModel).all()


@app.put(
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
# ACTIVIDADES - CRUD
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

    # Asegurar que el tarea_id enviado coincida con la URL
    if actividad.tarea_id != tarea_id:
        raise HTTPException(
            status_code=400,
            detail="El tarea_id del cuerpo debe coincidir con el de la URL"
        )

    db_actividad = ActividadModel(
        **actividad.model_dump()
    )

    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)

    return db_actividad


@app.get(
    "/actividades/",
    response_model=List[ActividadRespuesta]
)
def listar_actividades(
    db: Session = Depends(get_db)
):
    return db.query(ActividadModel).all()


@app.put(
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


@app.patch(
    "/actividades/{actividad_id}/completada",
    response_model=ActividadRespuesta
)
def cambiar_completada(
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

    db_actividad.completada = not db_actividad.completada

    db.commit()
    db.refresh(db_actividad)

    return db_actividad


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