from typing import Optional
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name:str
    email:str
    password:str

#Cuando el valor puede ser nulo
#email2:Optional[str]=None

#Las validaciones se pone dentro de los modelos