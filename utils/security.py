from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer
from utils.jwt import verificar_token

security=HTTPBearer()

def obtener_usuario_actual(credentials=Depends(security)):
    token=credentials.credentials
    payload=verificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401,detail="Token invalido")
    return payload