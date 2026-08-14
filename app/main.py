from fastapi import FastAPI, HTTPException
from typing import List

from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta
from app.schemas.tarea import TareaCrear, TareaRespuesta
from app.schemas.actividad import ActividadCrear, ActividadRespuesta


app = FastAPI(
    title="API de Gestión de Tareas - Versión Memoria",
    description="Proyecto ADSO - Persistencia en memoria",
    version="1.0.0"
)


# =========================================================
# BASES DE DATOS EN MEMORIA
# =========================================================

usuarios = []
tareas = []
actividades = []


# Contadores para generar IDs
contador_usuario = 1
contador_tarea = 1
contador_actividad = 1


# =========================================================
# INICIO
# =========================================================

@app.get("/")
def leer_raiz():
    return {
        "mensaje": "Bienvenido a la API de Gestión de Tareas - Versión Memoria"
    }


# =========================================================
# USUARIOS
# =========================================================

@app.post(
    "/usuarios/",
    response_model=UsuarioRespuesta,
    status_code=201
)
def crear_usuario(usuario: UsuarioCrear):

    global contador_usuario

    # Validar que el correo sea único
    for usuario_existente in usuarios:
        if usuario_existente["correo"] == usuario.correo:
            raise HTTPException(
                status_code=409,
                detail="El correo ya está registrado"
            )

    nuevo_usuario = {
        "id": contador_usuario,
        "nombre": usuario.nombre,
        "correo": usuario.correo
    }

    usuarios.append(nuevo_usuario)
    contador_usuario += 1

    return nuevo_usuario


@app.get(
    "/usuarios/",
    response_model=List[UsuarioRespuesta]
)
def listar_usuarios():
    return usuarios


# =========================================================
# TAREAS
# =========================================================

@app.post(
    "/tareas/",
    response_model=TareaRespuesta,
    status_code=201
)
def crear_tarea(tarea: TareaCrear):

    global contador_tarea

    # Validar que el usuario exista
    usuario = None

    for usuario_existente in usuarios:
        if usuario_existente["id"] == tarea.usuario_id:
            usuario = usuario_existente
            break

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario asignado no existe"
        )

    nuevo_usuario = usuario.copy()

    nueva_tarea = {
        "id": contador_tarea,
        "nombre": tarea.nombre,
        "descripcion": tarea.descripcion,
        "estado": tarea.estado,
        "avance": tarea.avance,
        "fecha_inicio": tarea.fecha_inicio,
        "fecha_final": tarea.fecha_final,
        "usuario_id": tarea.usuario_id,
        "usuario": nuevo_usuario
    }

    tareas.append(nueva_tarea)
    contador_tarea += 1

    return nueva_tarea


@app.get(
    "/tareas/",
    response_model=List[TareaRespuesta]
)
def listar_tareas():
    return tareas


# =========================================================
# ACTIVIDADES
# =========================================================

@app.post(
    "/tareas/{tarea_id}/actividades/",
    response_model=ActividadRespuesta,
    status_code=201
)
def crear_actividad(
    tarea_id: int,
    actividad: ActividadCrear
):

    global contador_actividad

    # Validar que la tarea exista
    tarea = None

    for tarea_existente in tareas:
        if tarea_existente["id"] == tarea_id:
            tarea = tarea_existente
            break

    if tarea is None:
        raise HTTPException(
            status_code=404,
            detail="La tarea asignada no existe"
        )

    # Validar que el ID enviado coincida con el de la URL
    if actividad.tarea_id != tarea_id:
        raise HTTPException(
            status_code=400,
            detail="El tarea_id debe coincidir con el de la URL"
        )

    nueva_actividad = {
        "id": contador_actividad,
        "nombre": actividad.nombre,
        "descripcion": actividad.descripcion,
        "estado": actividad.estado,
        "fecha": actividad.fecha,
        "completada": actividad.completada,
        "tarea_id": tarea_id
    }

    actividades.append(nueva_actividad)
    contador_actividad += 1

    return nueva_actividad


@app.get(
    "/actividades/",
    response_model=List[ActividadRespuesta]
)
def listar_actividades():
    return actividades


# =========================================================
# ACTUALIZAR ACTIVIDAD
# =========================================================

@app.patch(
    "/actividades/{actividad_id}",
    response_model=ActividadRespuesta
)
def actualizar_actividad(actividad_id: int):

    for actividad in actividades:

        if actividad["id"] == actividad_id:

            # Cambiar True por False o False por True
            actividad["completada"] = not actividad["completada"]

            return actividad

    raise HTTPException(
        status_code=404,
        detail="Actividad no encontrada"
    )