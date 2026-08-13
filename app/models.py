from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)

    # Relación con tareas
    tareas = relationship("TareaModel", back_populates="usuario", cascade="all, delete-orphan")


class TareaModel(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, nullable=False)
    avance = Column(Float, default=0.0)
    fecha_inicio = Column(Date, nullable=False)
    fecha_final = Column(Date, nullable=False)
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # Relaciones
    usuario = relationship("UsuarioModel", back_populates="tareas")
    actividades = relationship("ActividadModel", back_populates="tarea", cascade="all, delete-orphan")


class ActividadModel(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, nullable=False)
    fecha = Column(Date, nullable=False)
    completada = Column(Boolean, default=False)
    
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=False)

    # Relación con tarea
    tarea = relationship("TareaModel", back_populates="actividades")