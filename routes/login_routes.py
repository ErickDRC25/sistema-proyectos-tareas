from fastapi import APIRouter,HTTPException
from schemas.login_schema import Login
from config.db import engine,UsuarioTable
from routes.usuarios_routes import verify_password
from utils.jwt import crear_token

loginrouter=APIRouter()

@loginrouter.post("/login")
def login(data:Login):
    with engine.connect() as conn:
        usuario=conn.execute(UsuarioTable.select().where(UsuarioTable.c.email==data.email)).first()
        if not usuario:
            raise HTTPException(status_code=401,detail="credenciales incorrectas")
            
        
        usuario_dict=usuario._asdict()
        if not verify_password(data.password,usuario_dict['password']):
            raise HTTPException(status_code=401,detail="credenciales incorrectas")

        token=crear_token({
            "id":str(usuario_dict['id']),
            "rol":usuario_dict['rol']
        })
        
        return{
            "access_token":token,
            "token_type":"bearer"
        }