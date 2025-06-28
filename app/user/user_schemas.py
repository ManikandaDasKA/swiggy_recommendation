from pydantic import BaseModel
from typing import *
from app.models import Users,Orders


class UserCreate(BaseModel):
    user_id:int
    name:str
    age:int
    gender:str
    marital_status:str
    occupation:str
    usercity:Optional[str]

class UserUpdate(BaseModel):
    user_id:int
    name:Optional[str]
    age:Optional[int]
    gender:Optional[str]
    marital_status:Optional[str]
    occupation:Optional[str]
    usercity:Optional[str]

class UserList(BaseModel):
    user_list:List[Users]

class OrdersCreate(BaseModel):
    o_id:int
    order_date:str
    sales_qty:int
    sales_amount:int
    currency:str
    user_id:int
    r_id:int
    order_city:str

class Orders_list(BaseModel):
    orders_list:List[Orders]