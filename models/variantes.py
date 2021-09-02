from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, String, ARRAY, Float, Date, LargeBinary
from config.db import meta

variantes= Table(
    'variantes',meta,
    Column('id_variante',Integer,primary_key=True),
    Column('nombre',String(100)),
    Column('color',String(10))
)