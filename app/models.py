from sqlmodel import SQLModel,Field,Relationship
from typing import *
from datetime import datetime

class Restaurant(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    rating: Optional[str] = Field(default=None)
    rating_count: Optional[str] = Field(default=None)
    cuisine: Optional[str] = Field(default=None)
    link: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)

    menu_items: List["Menu"] = Relationship(back_populates="rest_menu")

class Menu(SQLModel, table=True):
    m_id: Optional[int] = Field(primary_key=True, default=None)
    menu_id: str = Field(default=None)
    r_id: int = Field(foreign_key="restaurant.id")
    f_id: str = Field(foreign_key="food.f_id")
    cuisine: str = Field(default=None)
    price: float = Field(default=None)

    rest_menu: Optional["Restaurant"] = Relationship(back_populates="menu_items")
    food_item: Optional["Food"] = Relationship(back_populates="menus")


class Food(SQLModel, table=True):
    f_id: str = Field(primary_key=True, default=None)
    item: str = Field(default=None)
    veg_or_non_veg: str = Field(default=None)

    menus: List["Menu"] = Relationship(back_populates="food_item")


class Users(SQLModel,table=True):
    user_id:int= Field(primary_key=True,default=None) 
    name:str = Field(default=None)
    age:int = Field(default=None)
    gender:str = Field(default=None)
    marital_status:str = Field(default=None)
    occupation:str = Field(default=None)
    usercity:Optional[str] = Field(default=None)

class Orders(SQLModel,table=True):
    o_id:Optional[int] = Field(primary_key=True,default=None)  
    order_date:Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%d-%b-%y"))
    sales_qty:int = Field(default=None)
    sales_amount:int = Field(default=None)
    currency:str = Field(default=None)

    user_id: int = Field(foreign_key="users.user_id")
    r_id: Optional[int] = Field(default=None, foreign_key="restaurant.id")
    order_city: Optional[str] = Field(default=None)

    user: Optional["Users"] = Relationship()
    restaurant: Optional["Restaurant"] = Relationship()

