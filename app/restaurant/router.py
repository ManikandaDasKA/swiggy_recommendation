from fastapi import APIRouter, Depends
from app.restaurant.schemas import RestaurantCreate, RestaurantList, RestaurantUpdate,MenuCreate,RestaurantMenuList,MenuUpdate,RestaurantMenuSchema,RestaurantandMenuList, MenuWithFoodSchema,RestaurantandMenuList, FoodSchema
from sqlmodel import Session,select
from app.models import Restaurant,Menu,Food
from app.database import get_session
from typing import *
from sqlalchemy.sql.operators import ilike_op
# import re
# from sqlalchemy.orm import selectinload

app = APIRouter(prefix="")

@app.post("/restaurant_create")
def restaurant_create(restaurant_request:RestaurantCreate,session:Session=Depends(get_session)):

  restaurant = Restaurant(id = restaurant_request.id,
                            name=restaurant_request.name,
                            country = restaurant_request.country,
                            city=restaurant_request.city,
                            rating=restaurant_request.rating,
                            rating_count=restaurant_request.rating_count,
                            cuisine=restaurant_request.cuisine,
                            link=restaurant_request.link,
                            address=restaurant_request.address)
  session.add(restaurant)
  session.commit()
  session.refresh(restaurant)

  return{"message":"restaurant successfully created", "data":restaurant.model_dump(),"errorcode":0}

@app.post("/restaurant_list")
def list_restaurants(session: Session = Depends(get_session)):
    stmt= select(Restaurant)
    restaurants = session.exec(stmt).all()
    restaurant_list_schema = RestaurantList(restaurant_list=restaurants)
    
    return{"message":"resturant list created successfully",
          "data":restaurant_list_schema.model_dump(),
          "errorcode":0}

@app.get("/restaurant/search")
def restaurant_search(name:str,session:Session=Depends(get_session)):
   stmt = select(Restaurant).where(ilike_op(Restaurant.name,f'{name}%'))
   rest_found:List[Restaurant] = session.exec(stmt).all()

   if len(rest_found)>0:
      rest_list = RestaurantList(restaurant_list=rest_found)
      
      return {"errorcode":0,"data":rest_list.model_dump(),"message":"success"}
   else:
      return {"errorcode":1,"data":{},"message":f"no restaurants found under {name}"}
   
   

@app.post("/restaurant_update")
def update_restaurant(restaurant_request:RestaurantUpdate,session:Session=Depends(get_session)):
   stmt=select(Restaurant).where(Restaurant.id == restaurant_request.id)
   restaurant=session.exec(stmt).first()

   if restaurant:
      if restaurant_request.name:
         restaurant.name = restaurant_request.name
      if restaurant_request.country:
         restaurant.country = restaurant_request.country
      if restaurant_request.city:
         restaurant.city =  restaurant_request.city
      if restaurant_request.rating:
         restaurant.rating =  restaurant_request.rating
      if restaurant_request.rating_count:
         restaurant.rating_count =  restaurant_request.rating_count
      if restaurant_request.cuisine:
         restaurant.cuisine =  restaurant_request.cuisine
      if restaurant_request.link:
         restaurant.link =  restaurant_request.link
      if restaurant_request.address:
         restaurant.address =  restaurant_request.address

      session.add(restaurant)
      session.commit()
      session.refresh(restaurant)

      return{"Errorcode":0,"data":restaurant.model_dump(),"message":"Success"}
   else:
      return{"Errorcode":1,"data":{},"message":"can't add this restaurant"}
   

@app.post("/restaurant/delete")
def get_restaurant_delete(id: int, session:Session = Depends(get_session)):
  stmt= select(Restaurant).where(Restaurant.id == id)
  restaurant:Optional[Restaurant]=session.exec(stmt).first()
  if restaurant:
    session.delete(restaurant)
    session.commit()
    return{"message":"restaurant deleted successful",
        "errorcode":0}
  else:
      return{"message":"restaurant not fund",
        "errorcode":1}
  
   
@app.post("/restaurant/menu/create")
def restaurant_menu_create(restaurant_menu_request:MenuCreate,session:Session=Depends(get_session)):
    restaurantmenu = Menu(menu_id=restaurant_menu_request.menu_id,
                          r_id=restaurant_menu_request.r_id,
                          f_id=restaurant_menu_request.f_id,
                          cuisine=restaurant_menu_request.cuisine,
                          price=restaurant_menu_request.price)
    
    session.add(restaurantmenu)
    session.commit()
    session.refresh(restaurantmenu)
    return {"message":"restaurant menu create successfully","data":restaurantmenu.model_dump(),"errorcode":0}


@app.post("/restaurant/menu/list")
def get_restaurant_menu_list(session:Session = Depends(get_session)):
  stmt= select(Menu)
  restaurant_menu_list:List[Menu]=session.exec(stmt)
  restaurant_menu_list_schema = RestaurantMenuList(restaurant_menu_list=restaurant_menu_list)
  return{"message":"restaurant list successful",
        "data":restaurant_menu_list_schema.model_dump(),
        "errorcode":0}

@app.post("/restaurant/menu/update")
def restaurant_menu_update(update_menu_data: MenuUpdate,session:Session=Depends(get_session)):
    stmt= select(Menu).where((Menu.menu_id == update_menu_data.menu_id) & (Menu.r_id == update_menu_data.r_id))
    menu:Optional[Menu]=session.exec(stmt).first()
    if menu:
        if update_menu_data.f_id:
            menu.f_id = update_menu_data.f_id
        if update_menu_data.cuisine:
            menu.cuisine= update_menu_data.cuisine
        if update_menu_data.price:
            menu.price = update_menu_data.price
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return {"message": "restaurant menu updated successfully", "data": menu.model_dump(),"errorcode": 0 }
    else:
        return {"message": "restaurant menu not found", "data": {},"errorcode": 1}

@app.post("/restaurant/menu/delete")
def get_restaurant_delete(menu_id: str, r_id:int, session:Session = Depends(get_session)):
  stmt= select(Menu).where((Menu.menu_id == menu_id) & (Menu.r_id == r_id))
  menu:Optional[Menu]=session.exec(stmt).first()
  if menu:
    session.delete(menu)
    session.commit()
    return{"message":"restaurant menu deleted successful",
        "errorcode":0}
  else:
      return{"message":"restaurant menu not fund",
        "errorcode":1}
  

@app.post("/restaurant/restaurantandmenu/list")
def get_restaurant_and_menu_list(session:Session = Depends(get_session)):
  statement = select(Restaurant)
  rest_all = session.exec(statement).all()
  print(rest_all)
  rests = [RestaurantMenuSchema(rest=rest,menu = rest.menu_item) for rest in rest_all]
  return {
        "message": "Restaurant list retrieved successfully","data": RestaurantandMenuList(restaurant_and_menu_list = rests),"errorcode": 0  }


# @app.post("/restaurant/restaurantandmenu/list")
# def get_restaurant_and_menu_list(session:Session = Depends(get_session)):
#   statement = select(Restaurant)
#   rest_all = session.exec(statement).all()

#   rests = [RestaurantMenuSchema(rest=rest,menu = rest.menu_item) for rest in rest_all]
#   return {
#         "message": "Restaurant list retrieved successfully","data": RestaurantandMenuList(restaurant_and_menu_list = rests),"errorcode": 0  }



# @app.get("/restaurant/menu/search")
# def restaurant_search(item_name:str,session:Session=Depends(get_session)):
#    stmt = select(Restaurant).join(Menu).where(ilike_op(Menu.item_name,f'{item_name}%'))
#    menu_found = session.exec(stmt).all()

#    if len(menu_found)>0:
#       menu_list =  [RestaurantMenuSchema(rest=found,menu = found.menu_item) for found in menu_found]
      
#       return {"errorcode":0,"data":RestaurantandMenuList(restaurant_and_menu_list = menu_list),"message":"success"}
#    else:
#       return {"errorcode":1,"data":{},"message":f"no restaurants found under {item_name}"}


# @app.get("/restaurant/menu/search")
# def restaurant_search(item_name: str, session: Session = Depends(get_session)):
#    stmt = (select(Restaurant).join(Menu).join(Food).where(ilike_op(Food.item, f"{item_name}%")))
#    menu_found = session.exec(stmt).all()
#    print(menu_found)
   
   # if len(menu_found)>0:
   #    menu_list =  [RestaurantMenuSchema(rest=found,menu = found.food_item) for found in menu_found]
  
   #    return {
   #       "errorcode": 0,
   #       "data": RestaurantandMenuList(restaurant_and_menu_list=menu_list),
   #       "message": "success"
   #    }
   # else:
   #    return {"errorcode": 1, "data": {}, "message": f"no restaurants found under {item_name}"}




# @app.get("/restaurant/menu/search")
# def restaurant_search(item_name: str, session: Session = Depends(get_session)):
#    stmt = (select(Restaurant,Menu,Food).where(ilike_op(Food.item, f"{item_name}%")))
#    menu_found = session.exec(stmt).all()
#    print(menu_found)




@app.get("/restaurant/menu/search", response_model=RestaurantandMenuList)
def restaurant_search(item_name: str, session: Session = Depends(get_session)):
    stmt = (
        select(Restaurant, Menu, Food)
        .join(Menu, Menu.r_id == Restaurant.id)
        .join(Food, Food.f_id == Menu.f_id)
        .where(Food.item.ilike(f"{item_name}%"))
    )
    results = session.exec(stmt).all()

    restaurant_map = {}

    for rest, menu, food in results:
        # Construct food schema
        food_schema = FoodSchema(
            f_id=food.f_id,
            item=food.item,
            veg_or_non_veg=food.veg_or_non_veg
        )

        # Construct menu with food schema
        menu_schema = MenuWithFoodSchema(
            menu_id=menu.menu_id,
            r_id=menu.r_id,
            f_id=menu.f_id,
            cuisine=menu.cuisine,
            price=menu.price,
            food_item=food_schema
        )

        if rest.id not in restaurant_map:
            restaurant_map[rest.id] = {
                "rest": rest,
                "menu": [menu_schema]
            }
        else:
            restaurant_map[rest.id]["menu"].append(menu_schema)

    response_data = [
        RestaurantMenuSchema(rest=entry["rest"], menu=entry["menu"])
        for entry in restaurant_map.values()
    ]

    return {"restaurant_and_menu_list": response_data}


