from pydantic import BaseModel
from typing import *
from app.models import Restaurant,Menu

class  RestaurantCreate(BaseModel):
    id:int
    name:str
    country:str
    city:str
    rating:str
    rating_count:str
    cuisine:str
    link:str
    address:str

class RestaurantUpdate(BaseModel):
    id:int
    name:Optional[str]
    country:Optional[str]
    city:Optional[str]
    rating:Optional[float]
    rating_count:Optional[str]
    cuisine:Optional[str]
    link:Optional[str]
    address:Optional[str]

class RestaurantList(BaseModel):
    restaurant_list:List[Restaurant]

# class ResturantAllResponse(BaseModel):
#     resturants:List[Restaurant] 
    
class MenuCreate(BaseModel):
    menu_id:str
    r_id:int
    f_id:str
    cuisine:str
    price:int

class RestaurantMenuList(BaseModel):
    restaurant_menu_list:List[Menu]

class MenuUpdate(BaseModel):
    menu_id:str
    r_id:int
    f_id:Optional[str]
    cuisine:Optional[str]
    price:Optional[int]

# class RestaurantMenuSchema(BaseModel):
#     rest:Restaurant
#     menu: List[Menu]

# class RestaurantandMenuList(BaseModel):
#     restaurant_and_menu_list: List[RestaurantMenuSchema]

class user_db_up(BaseModel):
    user_id:int
    name:str
    Age:int
    Gender:str
    Marital_Status:str
    Occupation:str
    UserCity:Optional[str]

class food(BaseModel):
    f_id:int
    item:str
    veg_or_non_veg:str

class order_db_up(BaseModel):
    o_id:int
    order_date:str
    sales_qty:int
    sales_amount:int
    currency:str
    user_id:int
    r_id:int
    Order_City:str



class FoodSchema(BaseModel):
    f_id: str
    item: str
    veg_or_non_veg: str

    # class Config:
    #     orm_mode = True

class MenuWithFoodSchema(BaseModel):
    menu_id: str
    r_id: int
    f_id: str
    cuisine: str
    price: float
    food_item: Optional[FoodSchema]

    # class Config:
    #     orm_mode = True


class RestaurantMenuSchema(BaseModel):
    rest: Restaurant
    menu: List[MenuWithFoodSchema]

    # class Config:
    #     orm_mode = True

class RestaurantandMenuList(BaseModel):
    restaurant_and_menu_list: List[RestaurantMenuSchema]
