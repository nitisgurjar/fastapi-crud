from tortoise.models import Model
from tortoise import Tortoise,fields


class Student(Model):
    id=fields.IntField(pk=True)
    name=fields.CharField(100)
    email=fields.CharField(100)
    phone=fields.CharField(10)
    password=fields.CharField(100)



Tortoise.init_models(['user.models'],'models')