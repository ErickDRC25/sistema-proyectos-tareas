from pydantic import BaseModel

class ProyectosCreate(BaseModel):
    nombre:str
    descripcion:str
    