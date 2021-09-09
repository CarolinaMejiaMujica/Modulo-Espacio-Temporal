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
from pydantic import BaseModel

tiempo = APIRouter()

def data_secuencias(ini,fin):
    df_secu=pd.DataFrame(conn.execute(f"select count(s.id_secuencia),s.fecha_recoleccion, v.nombre as variante, v.color from secuencias as s "+
            "LEFT JOIN agrupamiento as a ON s.id_secuencia=a.id_secuencia LEFT JOIN variantes as v ON a.id_variante=v.id_variante "+
            "LEFT JOIN algoritmos as m ON a.id_algoritmo=m.id_algoritmo "+
            "where m.nombre like 'k-means' and m.parametro=10 and "+
            "s.fecha_recoleccion >= \'"+ ini +"\' and s.fecha_recoleccion<= \'"+ fin +
            "\' group by s.fecha_recoleccion, v.nombre,v.color order by s.fecha_recoleccion").fetchall())
    df_secu.columns=['count','fecha','variante','color']
    return df_secu

@tiempo.post("/graficolineal/")
def grafico(fechaIni: str,fechaFin: str):
    df_secu=data_secuencias(fechaIni,fechaFin)
    fechas=list(set(df_secu['fecha']))
    variant=list(set(df_secu['variante']))
    for v in variant:
        fechas_variante=list(set(df_secu.loc[df_secu['variante']==v]['fecha']))
        for m in fechas:
            if m not in fechas_variante:
                df_secu=df_secu.append(pd.Series([0, m, v,df_secu.loc[df_secu['variante']==v]['color'].iloc[0]], index=df_secu.columns),ignore_index=True)

    colores=list()
    for a in list(set(df_secu['variante'])):
        colores.append(list(df_secu.color.loc[df_secu['variante']==a])[0])

    p = figure(tools="pan,zoom_in,zoom_out,undo,redo,reset,save",plot_width=1650, plot_height=500, x_axis_type="datetime")

    hover=HoverTool(tooltips=[('Fecha de recolección', '@fecha{%d-%m-%Y}'),
                            ("Cantidad de secuencias genómicas","@count"),
                            ("Variante",'@variante'),
                            ("Color","$variante $swatch:color")],formatters={'@fecha': 'datetime'})
    p.add_tools(hover)

    for name,color in zip(variant,colores):
        df = pd.DataFrame(df_secu.loc[df_secu['variante']==name].sort_values('fecha')).reset_index(drop=True)
        p.line('fecha','count',source=df, line_width=2, color=color, alpha=0.8,
            muted_color=color, muted_alpha=0.2, legend_label=name)

    p.legend.location = "top_left"
    p.legend.title = 'Variantes'
    p.legend.title_text_font_style = "bold"
    p.legend.title_text_font_size = "15px"
    p.legend.label_text_font_size = '11pt'
    p.legend.click_policy = "hide"
    p.xaxis.axis_label = "Mes-Año"
    p.yaxis.axis_label="Número de secuencias genómicas"
    p.xaxis.axis_label_text_font_style = "bold"
    p.yaxis.axis_label_text_font_style = "bold"
    p.xaxis.axis_label_text_font_size = "15px"
    p.yaxis.axis_label_text_font_size = "15px"
    p.xaxis.major_label_text_font_style="bold"
    p.yaxis.major_label_text_font_style="bold"
    p.xaxis.major_label_text_font_size="12px"
    p.yaxis.major_label_text_font_size="12px"
    p.xaxis.formatter=DatetimeTickFormatter(days=["%d-%m-%Y"],months=["%d-%m-%Y"],years=["%d-%m-%Y"])
    return json.dumps(json_item(p, "graficolineal"))


@tiempo.get("/graficocircular/")
def grafico(fechaIni: str,fechaFin: str):
    df_secu=data_secuencias(fechaIni,fechaFin)
    data=pd.DataFrame(df_secu.groupby(by=["variante","color"]).sum()[["count"]])
    data.rename(columns={"variante":"variante","color":"color","count":"count"})
    data=data.reset_index()
    data['angulo'] = data['count']/data['count'].sum()*2*pi
    data['pocentaje'] = round(data['count']/data['count'].sum()*100,2)

    p = figure(tools="pan,zoom_in,zoom_out,undo,redo,reset,save",plot_width=750, plot_height=600,
            tooltips=[("Variante","@variante"),("Porcentaje","@pocentaje{1.11} %"), ("Cantidad","@count")])

    p.wedge(x=0, y=1, radius=0.8,
            start_angle=cumsum('angulo', include_zero=True), end_angle=cumsum('angulo'),
            line_color="white", fill_color='color', legend_field='variante', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None

    p.legend.title = 'Variantes'
    p.legend.title_text_font_style = "bold"
    p.legend.title_text_font_size = "15px"
    p.legend.label_text_font_size = '11pt'
    p.legend.label_standoff = 2
    p.legend.glyph_width =20
    p.legend.glyph_height=20
    p.legend.spacing = 0
    p.legend.padding = 1
    p.legend.margin = 5
    return json.dumps(json_item(p, "graficocircular"))