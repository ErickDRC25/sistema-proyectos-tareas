from fastapi import APIRouter,Depends,HTTPException
from config.db import engine,UsuarioTable,ProyectoTable,MiembrosProyectoTable
from schemas.proyectos_schema import ProyectosCreate
from utils.security import obtener_usuario_actual
proyectosrouter=APIRouter()

@proyectosrouter.post("/proyectos")
def crear_proyecto(data:ProyectosCreate,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    
    if not data.nombre or data.nombre.strip()=="":
        raise HTTPException(status_code=400,detail="El campo nombre es obligatorio")
        
    if not data.descripcion or data.descripcion.strip()=="":
        raise HTTPException(status_code=400,detail="El campo descripcion es obligatorio")
        
    
    with engine.connect() as conn:
        proyecto_nuevo={
            "nombre":data.nombre,
            "descripcion":data.descripcion,
            "usuario_creador_id":idusuario
        }
        
        resultado=conn.execute(ProyectoTable.insert().values(proyecto_nuevo))
        
        
        nuevo_miembro={
            "usuario_id":idusuario,
            "rol_proyecto":"admin",
            "proyecto_id":resultado.lastrowid
        }
        conn.execute(MiembrosProyectoTable.insert().values(nuevo_miembro))
        conn.commit()
        return {"message":"Proyecto creado con exito"}
        
        
    

        
    
@proyectosrouter.get("/proyectos")
def ver_proyectos(user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        resultado= conn.execute(ProyectoTable.select().where(ProyectoTable.c.usuario_creador_id==idusuario)).fetchall()
        return [row._asdict() for row in resultado]
    
    
@proyectosrouter.put("/proyectos/{idProyecto}")
def actualizar_proyecto(idProyecto:int , data:ProyectosCreate , user=Depends(obtener_usuario_actual)):
    idusuariocreador=int(user['id'])
    with engine.connect() as conn:
        proyecto_actualizado={
            "nombre":data.nombre,
            "descripcion":data.descripcion
        }
        resultado=conn.execute(ProyectoTable.update().where((ProyectoTable.c.id==idProyecto)&(ProyectoTable.c.usuario_creador_id==idusuariocreador)).values(proyecto_actualizado))
        if resultado.rowcount==0:
            raise HTTPException(status_code=403,detail="El proyecto no existe o no te pertenece")
            
        conn.commit()
        return {"message":"Proyecto actualizado"}
        
    
@proyectosrouter.delete("/proyectos/{idProyecto}")
def eliminar_proyecto(idProyecto:int,user=Depends(obtener_usuario_actual)):
    idusuariocreador=int(user['id'])
    with engine.connect() as conn:
        resultado=conn.execute(ProyectoTable.delete().where((ProyectoTable.c.id==idProyecto)&(ProyectoTable.c.usuario_creador_id==idusuariocreador)))
        if resultado.rowcount==0:
             raise HTTPException(status_code=403,detail="El proyecto no existe o no te pertenece")
        
        conn.commit()
        return {"message":"El proyecto ha sido eliminado correctamente"}
        
            