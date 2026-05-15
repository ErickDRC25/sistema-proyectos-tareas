from fastapi import APIRouter,Depends,HTTPException
from config.db import MiembrosProyectoTable,engine,ProyectoTable,UsuarioTable,TareasTable
from schemas.miembros_schema import Miembros_ProyectoCreate
from utils.security import obtener_usuario_actual
from sqlalchemy import select,func
miembrosrouter=APIRouter()

@miembrosrouter.post("/proyectos/{idProyecto}/miembros")
def agregar_miembros_proyecto(idProyecto:int,data:Miembros_ProyectoCreate,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        proyecto=conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==idProyecto)).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="Proyecto inexistente")
            
        
        if proyecto.usuario_creador_id != idusuario:
            raise HTTPException(status_code=403,detail="No eres el lider del proyeto")
            
        
        usuario=conn.execute(UsuarioTable.select().where(UsuarioTable.c.id==data.usuario_id)).first()
        if usuario is None:
            raise HTTPException(status_code=404,detail="Usuario no existente")
            
        
        usuario_existente_enproyecto=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==data.usuario_id)&(MiembrosProyectoTable.c.proyecto_id==idProyecto))).first()
        if usuario_existente_enproyecto is not None:
            raise HTTPException(status_code=409,detail="El usuario ya esta agregado al grupo")
            
        
        añadir_miembro={
            "usuario_id":data.usuario_id,
            "proyecto_id":idProyecto
        }
        
        conn.execute(MiembrosProyectoTable.insert().values(añadir_miembro))
        conn.commit()
        return {"message":"Se registro miembro correctamente"}
        
        
        
    
        
        
#GET /proyectos/{idProyecto}/miembros

@miembrosrouter.get("/proyectos/{idProyecto}/miembros")
def ver_miembros_proyectos(idProyecto:int):
    with engine.connect() as conn:
        proyecto= conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==idProyecto)).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="Proyecto inexistente")
            
        
        tablaunida=MiembrosProyectoTable.join(UsuarioTable,MiembrosProyectoTable.c.usuario_id==UsuarioTable.c.id).join(ProyectoTable,MiembrosProyectoTable.c.proyecto_id==ProyectoTable.c.id)
        query= select(
            UsuarioTable.c.id,
            UsuarioTable.c.nombre,
            UsuarioTable.c.email,
            MiembrosProyectoTable.c.rol_proyecto
        ).select_from(tablaunida).where(ProyectoTable.c.id==idProyecto)
        resultado=conn.execute(query).fetchall()
        return{
            "proyecto_id":proyecto.id,
            "nombre_proyecto":proyecto.nombre,
            "miembros":[row._asdict() for row in resultado]
        }


#GET /proyectos/{idProyecto}/dashboard

@miembrosrouter.get("/proyectos/{idProyecto}/dashboard")
def conteo_tareas(idProyecto:int):
    with engine.connect() as conn:
        proyecto=conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==idProyecto)).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="Proyecto inexistente")
        
        total_tareas = conn.execute(select(func.count()).select_from(TareasTable).where(TareasTable.c.proyecto_id == idProyecto)).scalar()
        pendientes = conn.execute(select(func.count()).select_from(TareasTable).where((TareasTable.c.proyecto_id == idProyecto) &(TareasTable.c.estado == "pendiente"))).scalar()
        en_progreso=conn.execute(select(func.count()).select_from(TareasTable).where((TareasTable.c.proyecto_id==idProyecto)&(TareasTable.c.estado=="en_progreso"))).scalar()
        completada=conn.execute(select(func.count()).select_from(TareasTable).where((TareasTable.c.proyecto_id==idProyecto)&(TareasTable.c.estado=="completada"))).scalar()
        return {
            "total_tareas": total_tareas,
            "pendientes": pendientes,
            "en_progreso": en_progreso,
            "completada": completada
        }
