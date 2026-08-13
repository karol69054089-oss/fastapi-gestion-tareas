from fastapi import FastAPI
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta
from app.schemas.tarea import TareaCrear, TareaRespuesta
from app.schemas.actividad import ActividadCrear, ActividadRespuesta


app = FastAPI()

# Base de datos en memoria
usuarios = []
tareas = []
actividades = []

# Contadores de ID
usuario_id_counter = 1
tarea_id_counter = 1
actividad_id_counter = 1


# ------------------- USUARIOS -------------------

@app.get("/usuarios/")
def obtener_usuarios():
    return usuarios


@app.post("/usuarios/")
def crear_usuario(usuario: UsuarioCrear):
    global usuario_id_counter

    nuevo_usuario = {
        "id": usuario_id_counter,
        "nombre": usuario.nombre,
        "correo": usuario.correo
    }

    usuarios.append(nuevo_usuario)
    usuario_id_counter += 1

    return nuevo_usuario



# ------------------- TAREAS -------------------

@app.post("/tareas/")
def crear_tarea(tarea: TareaCrear):
    global tarea_id_counter

    # Validar que el usuario exista
    usuario_existe = any(u["id"] == tarea.usuario_id for u in usuarios)

    if not usuario_existe:
        return {"error": "El usuario no existe"}

    nueva_tarea = {
        "id": tarea_id_counter,
        **tarea.model_dump()
    }

    tareas.append(nueva_tarea)
    tarea_id_counter += 1

    return nueva_tarea


@app.get("/tareas/")
def obtener_tareas():
    return tareas


# ------------------- ACTIVIDADES -------------------

# ------------------- ACTIVIDADES -------------------

@app.get("/actividades/")
def obtener_actividades():
    return actividades


@app.post("/tareas/{tarea_id}/actividades/")
def crear_actividad(tarea_id: int, actividad: ActividadCrear):
    global actividad_id_counter

    # Validar que la tarea exista
    tarea_existe = any(t["id"] == tarea_id for t in tareas)

    if not tarea_existe:
        return {"error": "La tarea no existe"}

    nueva_actividad = {
        "id": actividad_id_counter,
        **actividad.model_dump(),
        "tarea_id": tarea_id
    }

    actividades.append(nueva_actividad)
    actividad_id_counter += 1

    return nueva_actividad


@app.patch("/actividades/{actividad_id}")
def actualizar_actividad(actividad_id: int, actividad: ActividadCrear):

    for a in actividades:
        if a["id"] == actividad_id:
            a.update(actividad.model_dump())
            return a

    return {"error": "La actividad no existe"}