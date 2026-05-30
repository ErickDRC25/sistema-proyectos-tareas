from sqlalchemy import create_engine,Table,MetaData
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL= os.getenv("DB_URL")
metadata=MetaData()
engine=create_engine(DB_URL)
UsuarioTable=Table('usuarios',metadata,autoload_with=engine)
ProyectoTable=Table('proyectos',metadata,autoload_with=engine)
MiembrosProyectoTable=Table('miembros_proyecto',metadata,autoload_with=engine)
TareasTable=Table('tareas',metadata,autoload_with=engine)