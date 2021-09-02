from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, String, ARRAY, Float, Date, LargeBinary
from config.db import meta

modelos= Table(
    'modelos',meta,
    Column('id_modelo',Integer,primary_key=True),
    Column('nombre',String(30)),
    Column('parametro',Integer),
    Column('modelo_entrenado',LargeBinary)
)