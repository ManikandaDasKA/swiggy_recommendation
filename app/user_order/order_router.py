from fastapi import APIRouter, Depends, HTTPException
from app.models import Orders,Users,Menu,Restaurant
from app.database import get_session
from sqlmodel import Session,select
from datetime import datetime
from app.user_order.order_schemas import OrdersCreate
from sqlalchemy import text

orders_app = APIRouter(prefix="")

@orders_app.post("/orders/create")
def create_order(order_request:OrdersCreate, session: Session = Depends(get_session)):
    # Get the user
    user = session.exec(select(Users).where(Users.user_id == order_request.user_id)).first()
    # print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the menu
    menu = session.exec(select(Menu).where(Menu.m_id == order_request.menu_id)).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu item not found")

    # Get the restaurant
    restaurant = session.exec(select(Restaurant).where(Restaurant.id == menu.r_id)).first()

    # Create the order
    new_order = Orders(
        sales_qty=order_request.sales_qty,
        sales_amount=menu.price * order_request.sales_qty,
        currency="INR",
        user_id=user.user_id,
        r_id=restaurant.id if restaurant else None,
        order_city=user.usercity,
        order_date=datetime.now().strftime("%d-%b-%y")
    )
    
    session.execute(text("SELECT setval('orders_o_id_seq', (SELECT MAX(o_id) FROM orders))"))

    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return{"message":"restaurant successfully created", "data":new_order.model_dump(),"errorcode":0}