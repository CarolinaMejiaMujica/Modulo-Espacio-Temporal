from fastapi import APIRouter, Response
#from config.db import conn
#from models.user import users
#from schemas.index import User
#from fastapi import HTTPException
import json
#from bokeh.plotting import Figure
from bokeh.embed import json_item
#from bokeh.sampledata.autompg import autompg
#from numpy import cos, linspace
#from bokeh.io import show
#from bokeh.models import LogColorMapper
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.iris import flowers
#from fastapi.responses import JSONResponse
#from fastapi.encoders import jsonable_encoder
#import xmltojson
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from bokeh.embed import file_html
from bokeh.resources import CDN

user = APIRouter()

templates = Jinja2Templates(directory="templates")

'''@user.get('/seleccionar')
def read_data():
    return conn.execute(users.select()).fetchall()'''

@user.get('/select')
def grafico_mapa():
    colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
    colors = [colormap[x] for x in flowers['species']]

    p = figure(title = "Iris Morphology")
    p.xaxis.axis_label = 'Petal Length'
    p.yaxis.axis_label = 'Petal Width'

    p.circle(flowers["petal_length"], flowers["petal_width"],
            color=colors, fill_alpha=0.2, size=10)

    #output_file("iris.html", title="iris.py example")

    #with open("iris.html", "r") as html_file:
    #    html = html_file.read()
    #    json_ = xmltojson.parse(html)
    #show(p)
    #return json.dumps(json_item(p, "myplot"))
    html = file_html(p, CDN, "grafico")
    return HTMLResponse(content=html, status_code=200)

@user.get("/grafico")
def grafico():
    html_content="""
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


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


