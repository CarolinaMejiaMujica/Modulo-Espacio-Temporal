from fastapi import APIRouter, Response
from config.db import conn
from models.user import users
from models.departamentos import departamentos
from models.secuencias import secuencias
from schemas.index import User
from fastapi import HTTPException
import json
from bokeh.plotting import Figure
from bokeh.embed import json_item
from bokeh.sampledata.autompg import autompg
from numpy import cos, linspace
import pandas as pd
from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.iris import flowers
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bokeh.models import CategoricalColorMapper
from bokeh.models.tools import TapTool
from bokeh.models.callbacks import CustomJS

from bokeh.embed import file_html
from bokeh.resources import CDN

from faker import Factory

user = APIRouter()

templates = Jinja2Templates(directory="templates")

'''@user.get('/seleccionar')
def read_data():
    return conn.execute(users.select()).fetchall()'''

'''@user.get('/select')
def grafico_mapa():
    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    colors = [colormap[x] for x in flowers['species']]
    p = figure(title = "Iris Morphology")
    p.xaxis.axis_label = 'Petal Length'
    p.yaxis.axis_label = 'Petal Width'
    p.circle(flowers["petal_length"], flowers["petal_width"],
            color=colors, fill_alpha=0.2, size=10)
    return json.dumps(json_item(p, "myplot"))'''

@user.get("/mapa")
def grafico():
    df_departamentos=pd.DataFrame(conn.execute(departamentos.select()).fetchall())
    df_departamentos.columns=['ID', 'Nombre', 'latitud', 'longitud']
    fake = Factory.create()
    colores=list()
    for j in range(25):
        colores.append(fake.hex_color())
    
    cjs = """
    console.log('Tap');
    console.log(source.selected.indices);
    """
    fig = figure(tools="pan,zoom_in,zoom_out,undo,redo,reset,save",plot_width=800, plot_height=700,
                x_axis_location=None, y_axis_location=None,
                tooltips=[("Departamento", "@Nombre")])
    fig.grid.grid_line_color = None
    valor=fig.patches("longitud", "latitud", source=df_departamentos,
                fill_color={'field': 'Nombre', 'transform': CategoricalColorMapper(palette=colores, factors=df_departamentos['Nombre'].to_list())},
                fill_alpha=0.7, line_color="white", line_width=0.5,legend='Nombre')
    fig.legend.location = "bottom_left"
    fig.legend.title = 'Variantes'
    fig.legend.title_text_color='Black'
    fig.legend.title_text_font = 'Calibri'
    fig.legend.title_text_font_size = '14pt'
    fig.legend.label_standoff = 2
    fig.legend.glyph_width =10
    fig.legend.glyph_height=10
    fig.legend.label_text_font_size = '11pt'
    fig.legend.spacing = 0
    fig.legend.padding = 1
    fig.legend.margin = 1
    cb = CustomJS(args=dict(source=valor.data_source), code=cjs)
    ttool = TapTool(callback=cb)
    fig.tools.append(ttool)
    return json.dumps(json_item(fig, "mapa"))


'''@user.get('/{id}')
def read_data(id:int):
    valor = conn.execute(users.select().where(users.c.id == id)).fetchall()
    if valor:
        return conn.execute(users.select().where(users.c.id == id)).fetchall()
    else:
        return HTTPException(404,'User not found')
    
@user.post('/')
def write_data(user:User):
    conn.execute(users.insert().values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    return conn.execute(users.select()).fetchall()

@user.put('/{id}')
def update_data(id:int,user:User):
    conn.execute(users.update().values(
        name=user.name,
        email=user.email,
        password=user.password
    ).where(users.c.id == id))
    return conn.execute(users.select()).fetchall()

@user.delete('/{id}')
def delete_data(id:int):
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select()).fetchall()'''


