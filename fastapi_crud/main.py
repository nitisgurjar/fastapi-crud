from fastapi import FastAPI
from user import api as UserAPI
from user import router as UserRouter

from tortoise.contrib.fastapi import register_tortoise
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware


middleware = [
    Middleware(SessionMiddleware, secret_key='super-secret')
]


app = FastAPI(middleware=middleware)
app.include_router(UserAPI.app)
app.include_router(UserRouter.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


JWT_SECRET = 'myjwtsecret'


register_tortoise(
    app,
    db_url="postgres://postgres:Nitish@11@127.0.0.1/crud",
    modules={'models': ['user.models',]},
    generate_schemas=True,
    add_exception_handlers=True,
)