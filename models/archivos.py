from sqlalchemy import Table,Column
from sqlalchemy.sql.sqltypes import Integer, String, ARRAY, Float, Date, LargeBinary
from config.db import meta

archivos=Table(
    'archivos',meta,
    Column('id_archivo',Integer,primary_key=True),
    Column('preprocesamiento',LargeBinary),
    Column('pca',LargeBinary),
    Column('tsne',LargeBinary)
)