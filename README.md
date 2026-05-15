Sistema de Gestión de Proyectos y Tareas API

Descripción
API REST desarrollada con FastAPI para gestionar: 

Usuarios
Login con JWT 
Proyectos
Miembros de proyectos 
Tareas
Asignación de tareas 
Estados de tareas 
Dashboard de tareas 


Tecnologías utilizadas:
Python 
FastAPI 
SQLAlchemy Core 
JWT Authentication 
Pydantic 
SQLite / MySQL 
Passlib 


Funcionalidades
Usuarios:
Registro de usuarios 
Login 
Hash de contraseñas 

Proyectos:
Crear proyectos
Editar proyectos 
Eliminar proyectos 
Ver proyectos 


Miembros:
Agregar miembros a proyectos 
Ver miembros del proyecto


Tareas:
Crear tareas 
Asignar tareas 
Cambiar estados 
Ver tareas del proyecto
Ver mis tareas 

Dashboard:
Total de tareas 
Tareas pendientes 
Tareas en progreso 
Tareas completadas 

Seguridad:

Autenticación JWT 
Validación de permisos 
Validación de miembros por proyecto 
Uso de HTTPException

Cómo ejecutar el proyecto
pip install -r requirements.txt

Ejecutar servidor
uvicorn main:app --reload

Documentación Swagger   
http://127.0.0.1:8000/docs

Autor
Erick Diego Romero Cruz