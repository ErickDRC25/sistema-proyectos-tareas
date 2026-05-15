from fastapi import APIRouter,HTTPException
from config.db import engine,UsuarioTable
from passlib.context import CryptContext
from schemas.usuarios_schema import UsuarioCreate

pwd=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd.hash(password)

def verify_password(password_plano,password_hash):
    return pwd.verify(password_plano,password_hash)


usuarioroutes=APIRouter()

@usuarioroutes.post("/usuario")
def crear_usuario(data:UsuarioCreate):
    if not data.nombre or data.nombre.strip()=="":
        raise HTTPException(status_code=400,detail={"El campo nombre es obligatorio"})
    if not data.email or data.email.strip()=="":
        raise HTTPException(status_code=400,detail={"El campo email es obligatorio"})
    if not data.password or data.password.strip()=="":
        raise HTTPException(status_code=400,detail={"El campo password es obligatorio"})
    
    with engine.connect() as conn:
        email_existente= conn.execute(UsuarioTable.select().where(UsuarioTable.c.email==data.email)).first()
        if email_existente:
            raise HTTPException(status_code=409,detail={"Email ya existente"})
        
        usuario_nuevo={
            "nombre":data.nombre,
            "email":data.email,
            "password":hash_password(data.password)
        }
        
        conn.execute(UsuarioTable.insert().values(usuario_nuevo))
        conn.commit()
        return {"message":"Usuario creado correctamente"}
        
        


