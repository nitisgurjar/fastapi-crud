from fastapi import APIRouter,Request,status,Depends,Form
from.models import *
from . pydantic import Person,Login,Datta,Update,Token
from . pydantic import Token
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from json import JSONEncoder
import typing
import passlib


app = APIRouter()
SECRET = b'your-secret-key'
manager = LoginManager(SECRET, token_url='/user_login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



manager = LoginManager(SECRET, token_url='/login')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post('/')
async def register(data:Person):
    if await Student.exists(phone=data.phone):
        return{"status":False,"message":"mobile number already exist"}
    elif await Student.exists(email=data.email):
        return{"status":False,"message":"email already exist"}
    else:
        user_obj=await Student.create(name=data.name,email=data.email,phone=data.phone,password=get_password_hash(data.password))
        return user_obj
    

@app.get('/all/')
async def all():
    user_obj=await Student.all()
    return user_obj


@app.post('/daata/')
async def daata(data:Datta):
    user_obj = await Student.filter(id=data.id)
    return user_obj


@app.delete('/delete/')
async def delete(data:Datta):
    user_obj= await Student.filter(id=data.id).delete()
    return {"message":"user deleted"}


@app.put('/update/')
async def update(data:Update):
    user_obj= await Student.get(id=data.id)
    if not user_obj:
        return{"status":False,"message":"user not register"}
    else:
        user_obj=await Student.filter(id=data.id).update(name=data.name,email=data.email,phone=data.phone)
        return user_obj


@manager.user_loader() # type: ignore
async def load_user(email: str):
    if await Student.exists(email=email):
        user = await Student.get(email=email)
        return user

@app.post('/login/')
async def login(data: Login):
    email = data.email
    user = await load_user(email)
 
    if not user:
        return JSONResponse({'status': False, 'message': 'User not Registered'}, status_code=403)
    elif not verify_password(data.password, user.password):
        return JSONResponse({'status': False, 'message': 'Invalid password'}, status_code=403)
    access_token = manager.create_access_token(data={'sub': {'id': user.id}})
    new_dict = jsonable_encoder(user)
    new_dict.update({'access_token': access_token})
    return Token(access_token=access_token, token_type='bearer')