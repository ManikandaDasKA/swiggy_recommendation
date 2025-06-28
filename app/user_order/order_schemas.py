from pydantic import BaseModel
from typing import *
# from app.models import Users,Orders


class OrdersCreate(BaseModel):
    # o_id:int
    # order_date:str
    sales_qty:int
    # sales_amount:int
    # currency:str
    user_id:int
    menu_id:int
    # r_id:int
    # order_city:str


