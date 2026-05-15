from jose import jwt,JWTError
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRED=int(os.getenv("ACCESS_TOKEN_EXPIRED"))


def crear_token(data:dict):
    to_encoded=data.copy()
    expired=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRED)
    to_encoded.update({"exp":expired})
    
    token=jwt.encode(to_encoded,SECRET_KEY,algorithm=ALGORITHM)
    return token

def verificar_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if not payload:
            return {"message":"Token invalido"}
        return payload
    except JWTError as e:
        print(e)
        return None