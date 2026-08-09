from fastapi import FastAPI
from schemas.usuario import UsuarioCrear, UsuarioRespuesta

app = FastAPI()

usuarios = []

tareas = []

actividades = []


@app.get("/")
def inicio():
    return {"mensaje": "API de gestión de tareas funcionando"}


@app.post("/usuarios/", response_model=UsuarioRespuesta)
def crear_usuario(usuario: UsuarioCrear):
    nuevo_usuario = {
        "id": len(usuarios) + 1,
        "nombre": usuario.nombre,
        "correo": usuario.correo
    }

    usuarios.append(nuevo_usuario)

    return nuevo_usuario


@app.get("/usuarios/", response_model=list[UsuarioRespuesta])
def obtener_usuarios():
    return usuarios