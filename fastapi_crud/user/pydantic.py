from pydantic import BaseModel


class Person(BaseModel):
    name:str
    email:str
    phone:str
    password:str

class Datta(BaseModel):
    id:int

class Update(BaseModel):
    id:int
    name:str
    email:str
    phone:str

class Login(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"