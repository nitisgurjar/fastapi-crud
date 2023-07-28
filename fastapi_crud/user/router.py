from fastapi import APIRouter,status,Request,Form,Depends
from . models import *
from passlib.context import CryptContext
from fastapi_login import LoginManager
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import typing
from fastapi.encoders import jsonable_encoder


router=APIRouter()

SECRET = b'your-secret-key'



manager = LoginManager(SECRET, token_url='/login')


templates=Jinja2Templates(directory="user/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    print(request.session)
    return request.session.pop("_messages") if "_messages" in request.session else []


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

@router.get('/',response_class=HTMLResponse)
async def read(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@router.get('/login/',response_class=HTMLResponse)
async def loginn(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})



@router.post('/registration/',response_class=HTMLResponse)
async def registration(request:Request,name:str=Form(...),
                                       email:str=Form(...),
                                       phone:str=Form(...),
                                       password:str=Form(...)
                                       ):
    if await Student.filter(email=email).exists():
        flash(request,"email already exist")
        return RedirectResponse('/',status_code=status.HTTP_302_FOUND)
    elif await Student.filter(phone=phone).exists():
        flash(request,"phone number already exist")
        return RedirectResponse('/',status_code=status.HTTP_302_FOUND)
    else:
        await Student.create(name=name,email=email,phone=phone,password= get_password_hash(password))
        flash(request,"data added successfully")
        return RedirectResponse('/login/',status_code=status.HTTP_302_FOUND)
    
@manager.user_loader() # type: ignore
async def load_user(phone: str):
    if await Student.exists(phone=phone):
        user = await Student.get(phone=phone)
        return user

@router.post('/loginn/',response_class=HTMLResponse)
async def login(request:Request,phone:str=Form(...),
                                 password:str=Form(...)):
    phone=phone
    user=await load_user(phone)
    if not user:
        flash(request,"user not registered")
        return RedirectResponse('/login/',status_code=status.HTTP_404_NOT_FOUND)
    elif not verify_password(password,user.password):
        flash(request,"invalid password")
        return RedirectResponse('/login/',status_code=status.HTTP_406_NOT_ACCEPTABLE)
    access_token = manager.create_access_token(
        data=dict(sub=phone)
    )
    if "_messages" not in request.session:
        request.session['_messages'] = []
        new_dict = {"user_id": str(
            user.id), "phone": phone, "access_token": str(access_token)}
        request.session['_messages'].append(
            new_dict
        )
    
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)

     


@router.get('/table/',response_class=HTMLResponse)
async def read_userm(request:Request):
    user = await Student.all()
    return templates.TemplateResponse('table.html',{
        "user":user,
        "request":request
    })


@router.get('/delete/{id}',response_class=HTMLResponse)
async def delete(request:Request,id:int):
    await Student.filter(id=id).delete()
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)


@router.get("/update/{id}", response_class=HTMLResponse)
async def update_item(request: Request, id: int):
    user = await Student.get(id=id)
    return templates.TemplateResponse("update.html", {
        "request": request,
        "user": user
    })




@router.post("/updatee/", response_class=HTMLResponse)
async def update(request: Request, id: int = Form(...),
                 name: str = Form(...),
                 email: str = Form(...),
                 phone: str = Form(...),
                 ):
   
    await Student.filter(id=id).update(name=name,
                                      email=email,
                                      phone=phone
                                      )
    return RedirectResponse('/table/', status_code=status.HTTP_302_FOUND)
