from sqlalchemy import create_engine,Table,MetaData

metadata=MetaData()
engine=create_engine("mysql+pymysql://root:mysqladmin@localhost:3306/db_sistema_gestion_proyectos_tareas")
UsuarioTable=Table('usuarios',metadata,autoload_with=engine)
ProyectoTable=Table('proyectos',metadata,autoload_with=engine)
MiembrosProyectoTable=Table('miembros_proyecto',metadata,autoload_with=engine)
TareasTable=Table('tareas',metadata,autoload_with=engine)