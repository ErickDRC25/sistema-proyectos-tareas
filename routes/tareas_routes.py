from fastapi import APIRouter,Depends,HTTPException
from config.db import engine,TareasTable,ProyectoTable,UsuarioTable,MiembrosProyectoTable
from schemas.tareas_schema import TareasCreate,TareasAsignar,TareasEstado
from utils.security import obtener_usuario_actual
tareasrouter=APIRouter()

prioridad=['baja',
        'media',
        'alta']

@tareasrouter.post("/tareas/crear")
def crear_tareas(data:TareasCreate,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    if not data.titulo or data.titulo.strip()=="":
         raise HTTPException(status_code=400,detail="El campo titulo es obligatorio")
    
    if not data.prioridad in prioridad:
         raise HTTPException(status_code=400,detail="El campo prioridad es obligatorio")
    if not data.proyecto_id:
         raise HTTPException(status_code=400,detail="El campo proyecto_id es obligatorio")
    
    with engine.connect() as conn:
        proyecto=conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==data.proyecto_id)).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="Proyecto no encontrado")
        usuario_proyecto=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==idusuario)&(MiembrosProyectoTable.c.proyecto_id==data.proyecto_id))).first()
        if usuario_proyecto is None:
            raise HTTPException(status_code=403,detail="No perteneces a este proyecto, no puedes crear tareas en ella.No tienes permisos")
            
        
        tarea_nueva={
            "titulo":data.titulo,
            "descripcion":data.descripcion,
            "prioridad":data.prioridad,
            "proyecto_id":data.proyecto_id
        }
        
        conn.execute(TareasTable.insert().values(tarea_nueva))
        conn.commit()
        return {"message":"Tarea creada correctamente"}
       
   
@tareasrouter.put("/tareas/asignar/{idProyecto}/{idTarea}")
def asignar_tarea(idProyecto:int,idTarea:int,data:TareasAsignar,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        
        proyecto_existente=conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==idProyecto)).first()
        if proyecto_existente is None:
            raise HTTPException(status_code=404,detail="Proyecto no encontrado")
        
        
        
        
        lider=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==idusuario)&(MiembrosProyectoTable.c.proyecto_id==idProyecto))).first()
        if lider is None:
            raise HTTPException(status_code=403,detail="No perteneces a este proyecto, no puedes crear tareas en ella")
            
        if lider.rol_proyecto!='admin':
            raise HTTPException(status_code=403,detail="solo el admin del proyecto puede asignar tareas")
            
        
        tarea_existe_enproyecto=conn.execute(TareasTable.select().where((TareasTable.c.id==idTarea)&(TareasTable.c.proyecto_id==idProyecto))).first()
        if  tarea_existe_enproyecto is None:
            raise HTTPException(status_code=404,detail="La tarea no existe en el proyecto")
            
        
        
        miembro=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==data.asignado_a)&(MiembrosProyectoTable.c.proyecto_id==idProyecto))).first()
        if miembro is None:
            raise HTTPException(status_code=404,detail="Miembro no existente en proyecto")
            
        
        asignar={
            "asignado_a":data.asignado_a
        }
        
        conn.execute(TareasTable.update().where(TareasTable.c.id==idTarea).values(asignar))
        conn.commit()
        return {"message":"Se asigno correctamente la tarea"}
        
        
    
    
    
    
    
estados=['pendiente', 'en_progreso', 'completada']
@tareasrouter.put("/tarea/estado/{idProyecto}/{idTarea}")
def cambiar_estado(idProyecto:int,idTarea:int,data:TareasEstado,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        proyecto=conn.execute(ProyectoTable.select().where((ProyectoTable.c.id==idProyecto))).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="El proyecto no existe")
            
        
        miembro=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==idusuario)&(MiembrosProyectoTable.c.proyecto_id==idProyecto))).first()
        if miembro is None:
            raise HTTPException(status_code=403,detail="No perteneces al proyecto")
            
        
        
        tarea=conn.execute(TareasTable.select().where((TareasTable.c.id==idTarea)&(TareasTable.c.proyecto_id==idProyecto))).first()
        if tarea is None:
            raise HTTPException(status_code=404,detail="la tarea no existe en el proyecto")
        
        if ( miembro.rol_proyecto != "admin"and tarea.asignado_a != idusuario):
            raise HTTPException(status_code=403,detail="No eres el lider o el usuario asignado para cambiar")
             
        
        if not data.estado.lower() in estados:
            raise HTTPException(status_code=400,detail="Estado invalido , los correctos son : 'pendiente', 'en_progreso', 'completada'")
            
        
        estado_actualizar={"estado":data.estado.lower()}
        
        conn.execute(TareasTable.update().where(TareasTable.c.id==idTarea).values(estado_actualizar))
        conn.commit()
        
        return {"message":"Se cambio el estado correctamente"}
        
        
        
        
        
        
        
#ver tareas de un proyecto validando q pertenezcas al proyecto        
@tareasrouter.get("/tarea/ver/{idProyecto}")
def ver_tareas_deproyecto(idProyecto:int , user = Depends(obtener_usuario_actual) ):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        proyecto=conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==idProyecto)).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="El proyecto no existe")
            
        
        miembro=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==idusuario)&(MiembrosProyectoTable.c.proyecto_id==idProyecto))).first()
        if miembro is None:
            raise HTTPException(status_code=403,detail="No perteneces al proyecto")
            
        
        resultado=conn.execute(TareasTable.select().where(TareasTable.c.proyecto_id==idProyecto)).fetchall()
        return [row._asdict() for row in resultado] 
    

@tareasrouter.get("/tarea/mistareas/{idProyecto}")
def ver_mis_tareas(idProyecto:int,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        proyecto=conn.execute(ProyectoTable.select().where(ProyectoTable.c.id==idProyecto)).first()
        if proyecto is None:
            raise HTTPException(status_code=404,detail="Proyecto inexistente")
            
        
        miembro=conn.execute(MiembrosProyectoTable.select().where((MiembrosProyectoTable.c.usuario_id==idusuario)&(MiembrosProyectoTable.c.proyecto_id==idProyecto))).first()
        if miembro is None:
            raise HTTPException(status_code=403,detail="No perteneces al proyecto")
            
        
        resultado=conn.execute(TareasTable.select().where((TareasTable.c.asignado_a==idusuario)&(TareasTable.c.proyecto_id==idProyecto))).fetchall()
        return [row._asdict() for row in resultado] 
        
      
        

        
    