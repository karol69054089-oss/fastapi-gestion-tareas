 # FastAPI Gestión de Tareas

Proyecto desarrollado para el programa de formación **Análisis y Desarrollo de Software (ADSO)** del SENA.

## Descripción

API RESTful para la gestión de usuarios, tareas y actividades.

El proyecto fue desarrollado utilizando:

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Git
- GitHub

La aplicación permite crear, consultar, actualizar y eliminar usuarios, tareas y actividades.

## Estructura del proyecto

```text
fastapi-gestion-tareas/
│
├── app/
│   ├── schemas/
│   │   ├── usuario.py
│   │   ├── tarea.py
│   │   └── actividad.py
│   │
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── docs/
│   └── MER_Gestion_Tareas.drawio.png
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt