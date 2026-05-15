from fastapi import FastAPI
from routes.usuarios_routes import usuarioroutes
from routes.login_routes import loginrouter
from routes.proyectos_routes import proyectosrouter
from routes.miembros_routes import miembrosrouter
from routes.tareas_routes import tareasrouter
app=FastAPI()

app.include_router(usuarioroutes)
app.include_router(loginrouter)
app.include_router(proyectosrouter)
app.include_router(miembrosrouter)
app.include_router(tareasrouter)
