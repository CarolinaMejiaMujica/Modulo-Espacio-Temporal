from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, String, ARRAY, Float
from config.db import meta

departamentos = Table(
    'departamentos',meta,
    Column('id_departamento',Integer,primary_key=True),
    Column('nombre',String(100)),
    Column('latitud',ARRAY(Float)),
    Column('longitud',ARRAY(Float))
)