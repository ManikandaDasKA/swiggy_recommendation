from fastapi import APIRouter, Depends
from app.models import Users
from app.database import get_session
from sqlmodel import Session,select
from sqlalchemy.sql.operators import ilike_op
from app.user.user_schemas import UserList,UserUpdate

from typing import *

user_app = APIRouter(prefix="")

@user_app.post("/user_create")
def user_create(users_request:Users,session:Session=Depends(get_session)):
  users = Users(user_id = users_request.user_id,
                            name=users_request.name,
                            age = users_request.age,
                            gender =users_request.gender,
                            marital_status =users_request.marital_status,
                            occupation =users_request.occupation,
                            usercity =users_request.usercity)
  session.add(users)
  session.commit()
  session.refresh(users)

  return{"message":"restaurant successfully created", "data":users.model_dump(),"errorcode":0}


@user_app.get("/user/search")
def user_search(name:str,session:Session=Depends(get_session)):
   stmt = select(Users).where(ilike_op(Users.name,f'{name}%'))
   user_found:List[Users] = session.exec(stmt).all()

   if len(user_found)>0:
      users_list = UserList(user_list=user_found)
      
      return {"errorcode":0,"data":users_list.model_dump(),"message":"success"}
   else:
      return {"errorcode":1,"data":{},"message":f"no restaurants found under {name}"}
   


@user_app.post("/user_update")
def update_user(users_request:UserUpdate,session:Session=Depends(get_session)):
   stmt=select(Users).where(Users.user_id == users_request.user_id)
   users=session.exec(stmt).first()

   if users:
      if users_request.name:
        users.name = users_request.name
      if users_request.age:
         users.age = users_request.age
      if users_request.gender:
         users.gender =  users_request.gender
      if users_request.marital_status:
         users.marital_status = users_request.marital_status
      if users_request.occupation:
         users.occupation =  users_request.occupation
      if users_request.usercity:
         users.usercity =  users_request.usercity

      session.add(users)
      session.commit()
      session.refresh(users)

      return{"Errorcode":0,"data":users.model_dump(),"message":"Success"}
   else:
      return{"Errorcode":1,"data":{},"message":"can't add this restaurant"}
   

@user_app.post("/user/delete")
def get_user_delete(userid: int, session:Session = Depends(get_session)):
  stmt= select(Users).where(Users.user_id == userid)
  users:Optional[Users]=session.exec(stmt).first()
  if users:
    session.delete(users)
    session.commit()
    return{"message":"restaurant deleted successful",
        "errorcode":0}
  else:
      return{"message":"restaurant not fund",
        "errorcode":1}
  