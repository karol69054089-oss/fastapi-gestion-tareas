# FastAPI Gestión de Tareas

Proyecto desarrollado para el programa de formación Análisis y Desarrollo de Software (ADSO) - SENA.

## Descripción
API RESTful diseñada para gestionar Usuarios, Tareas y Actividades, utilizando una arquitectura modular con FastAPI, SQLAlchemy y PostgreSQL.

## Estructura del Proyecto
- `/app`: Código fuente principal.
  - `/schemas`: Modelos de validación (Pydantic).
  - `models.py`: Entidades de base de datos (SQLAlchemy).
  - `database.py`: Configuración de conexión y sesión.
  - `main.py`: Endpoints y lógica de la API.

---

## Diagrama Entidad-Relación (MER)
![MER](/docs/MER_Gestion_Tareas.drawio.png)

---

## Proceso de Desarrollo
1. **Fase 1 (main):** Documentación inicial, creación del diagrama MER y configuración del entorno de trabajo.
2. **Fase 2 (v-memoria):** Desarrollo de la lógica de negocio simulada en memoria (ramas y diccionarios).
3. **Fase 3 (v-postgres):** Migración a base de datos relacional PostgreSQL, implementación de ORM con SQLAlchemy, inyección de dependencias y variables de entorno (`.env`).

---

## Instalación y Configuración
1. Clonar el repositorio: 
   ```bash
   git clone <url-de-tu-repo>