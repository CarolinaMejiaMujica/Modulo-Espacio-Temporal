from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer
from config.db import meta

agrupamiento= Table(
    'agrupamiento',meta,
    Column('id_agrupamiento',Integer,primary_key=True),
    Column('id_modelo',Integer),
    Column('id_secuencia',Integer),
    Column('id_variante',Integer),
    Column('num_cluster',Integer)
)