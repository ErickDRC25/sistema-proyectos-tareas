from pydantic import BaseModel

class TareasCreate(BaseModel):
    titulo:str
    descripcion:str
    prioridad:str
    proyecto_id:int
    
class TareasAsignar(BaseModel):
    asignado_a:int
    
class TareasEstado(BaseModel):
    estado:str