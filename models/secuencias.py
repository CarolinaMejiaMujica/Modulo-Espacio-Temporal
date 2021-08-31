from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, String, ARRAY, Float, Date, LargeBinary
from config.db import meta

secuencias = Table(
    'secuencias',meta,
    Column('id_secuencia',Integer,primary_key=True),
    Column('codigo',String(25)),
    Column('secuencia',String(30000)),
    Column('fecha_recoleccion',Date),
    Column('secuencia_alineada',String(30000)),
    Column('id_departamento',Integer)
)