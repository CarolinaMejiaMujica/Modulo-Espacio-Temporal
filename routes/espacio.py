from fastapi import APIRouter, Response
from config.db import conn
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
from bokeh.plotting import figure, show,  output_file, save
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from bokeh.models import CategoricalColorMapper
from bokeh.models.tools import TapTool
from bokeh.models.callbacks import CustomJS
from bokeh.embed import file_html
from bokeh.resources import CDN
from bokeh.models import DatetimeTickFormatter
from bokeh.models import HoverTool
from math import pi
from bokeh.transform import cumsum


espacio = APIRouter()

@espacio.get("/mapa")
def grafico():
    df_departamentos=pd.DataFrame(conn.execute(departamentos.select()).fetchall())
    df_departamentos.columns=['ID', 'Nombre', 'latitud', 'longitud']
    df_dep=pd.DataFrame(conn.execute(f"select count(s.id_secuencia) AS count, d.nombre from departamentos as d LEFT JOIN secuencias as s ON d.id_departamento=s.id_departamento LEFT JOIN agrupamiento as a ON s.id_secuencia=a.id_secuencia LEFT JOIN variantes as v ON a.id_variante=v.id_variante LEFT JOIN modelos as m ON a.id_modelo=m.id_modelo and m.nombre like 'k-means' group by d.nombre order by d.nombre").fetchall())
    df_dep.columns=['count','Nombre']
    df_departamentos = pd.merge(df_departamentos, df_dep, on='Nombre')
    df_departamentos["variantes"] = ""
    df_departamentos["variante"] = ""
    df_vari=pd.DataFrame(conn.execute(f"SELECT d.nombre, COALESCE(v.id_variante,0) as id_variante, count(a.*), COALESCE(v.nombre,'') as nombre_variante, v.color from departamentos as d LEFT JOIN secuencias as s ON d.id_departamento=s.id_departamento LEFT JOIN agrupamiento as a ON s.id_secuencia=a.id_secuencia LEFT JOIN variantes as v ON a.id_variante=v.id_variante LEFT JOIN modelos as m ON a.id_modelo=m.id_modelo and m.nombre like 'k-means' GROUP BY d.nombre,v.id_variante ORDER BY d.nombre ASC").fetchall())
    df_vari.columns=['Nombre','id_variante','count_variante','nombre_variante','color']
    df_departamentos['color']=''
    for i,d in enumerate(df_departamentos['Nombre']):
        var_dep=list((df_vari.loc[df_vari['Nombre']==d]['nombre_variante']).unique())
        variante_pred=(df_vari.loc[df_vari['Nombre']==d].max())['nombre_variante']
        if len(variante_pred)==0:
            df_departamentos['variantes'][i]='No hay datos'
            df_departamentos['variante'][i]='No hay datos'
            df_departamentos['color'][i]='#CDCDCD'
        else:
            df_departamentos['variantes'][i]=var_dep
            df_departamentos['variante'][i]=variante_pred
            df_departamentos['color'][i]=list(df_vari.loc[df_vari['nombre_variante']==variante_pred]['color'])[0]
    cjs = """
    console.log('Tap');
    console.log(source.selected.indices);
    var valor=source.selected.indices
    """
    TOOLTIPS=[("Departamento", "@Nombre"),
            ("Total de secuencias genómicas", "@count"),
            ("Variantes identificadas","@variantes"),
            ("Variante predominante","@variante"),
            ("Color", "$variante $swatch:color")]

    fig = figure(tools="pan,zoom_in,zoom_out,undo,redo,reset,save",plot_width=700, plot_height=650,
                x_axis_location=None, y_axis_location=None,tooltips=TOOLTIPS)

    fig.grid.grid_line_color = None
    valor=fig.patches("longitud", "latitud", source=df_departamentos,
                fill_color={'field': 'variante', 'transform': CategoricalColorMapper(palette=df_departamentos['color'], factors=df_departamentos['variante'].to_list())},
                fill_alpha=0.7, line_color="white", line_width=0.5,legend='variante')

    fig.legend.location = "bottom_left"
    fig.legend.title = 'Variantes'
    fig.legend.title_text_font_style = "bold"
    fig.legend.title_text_font_size = "15px"
    fig.legend.label_text_font_size = '11pt'
    fig.legend.label_standoff = 2
    fig.legend.glyph_width =20
    fig.legend.glyph_height=20
    fig.legend.spacing = 0
    fig.legend.padding = 1
    fig.legend.margin = 5

    cb = CustomJS(args=dict(source=valor.data_source), code=cjs)
    ttool = TapTool(callback=cb)
    fig.tools.append(ttool)
    return json.dumps(json_item(fig, "mapa"))