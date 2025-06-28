from sqlmodel import Session, create_engine
from app.models import SQLModel
from app.config import settings
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from pathlib import Path
import csv
# from database import get_session

# import mysql.connector

DATABASE_URL = settings.DATABASE_URL
# CONNECTION_STRING = settings.CONNECTION_STRING
DB_NAME = settings.DB_NAME
DB_USER = settings.DB_USER
DB_PORT = settings.DB_PORT
DB_PASSWORD = settings.DB_PASSWORD
DB_HOST = settings.DB_HOST

engine = create_engine(DATABASE_URL,echo=True)

# engine = create_engine(CONNECTION_STRING, echo=True)

# Step 1: Create PostgreSQL database if it doesn't exist
def create_postgres_database(dbname, user, password, host="localhost", port=5432):
    try:
        con = psycopg2.connect(dbname="postgres", user=user, password=password, host=host, port=port)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{dbname}'")
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{dbname}"')
            # return{"message":"Database '{dbname}' created successfully."}
            # return dbname
        else:
            cur.close()
            con.close()
            # return{"message":"Database '{dbname}' already exists."}
        
    except Exception as e:
        return{"Error creating database: {e}"}

def call_database():
    create_postgres_database(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_data():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()

    csv1=Path("C:\\Swiggy clone\\restaurant.csv")
    csv2 = Path("C:\\Swiggy clone\\food.csv")
    csv3 =Path("C:\\Swiggy clone\\menu.csv")
    csv4 =Path("C:\\Swiggy clone\\users.csv")
    csv5 =Path("C:\\Swiggy clone\\orders.csv")
    
    dict_list = list()
    with csv1.open(mode="r",encoding="utf-8") as csv_reader1:
        csv_reader1 = csv.reader(csv_reader1)
        next(csv_reader1)  # Skip the header row
        for rows in csv_reader1:
            dict_list.append({'id':rows[0], 'name':rows[1], 'country':rows[2],'city':rows[3], 'rating':rows[4], 'rating_count':rows[5],'cuisine':rows[6], 'link':rows[7], 'address':rows[8]})
            for item in dict_list:
                sql = "INSERT INTO restaurant(id, name, country, city,rating,rating_count,cuisine,link,address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = item['id'], item['name'], item['country'], item['city'], item['rating'], item['rating_count'], item['cuisine'], item['link'], item['address']
                cursor.execute(sql, val)
                dict_list.clear()
            dict_list.clear()
            conn.commit()
            
    dict_list = list()
    with csv2.open(mode="r",encoding="utf-8") as csv_reader2:
        csv_reader2 = csv.reader(csv_reader2)
        next(csv_reader2)  # Skip the header row
        for rows in csv_reader2:
            dict_list.append({'f_id':rows[0], 'item':rows[1], 'veg_or_non_veg':rows[2]})
            for item in dict_list:
                sql = "INSERT INTO food(f_id, item, veg_or_non_veg) VALUES (%s, %s, %s)"
                val = item['f_id'], item['item'], item['veg_or_non_veg']
                cursor.execute(sql, val)
                dict_list.clear()
            dict_list.clear()
            conn.commit()


    dict_list = list()
    with csv3.open(mode="r",encoding="utf-8") as csv_reader3:
        csv_reader3 = csv.reader(csv_reader3)
        next(csv_reader3)  # Skip the header row
        for rows in csv_reader3:
            dict_list.append({'m_id':rows[0], 'menu_id':rows[1], 'r_id':rows[2], 'f_id':rows[3],'cuisine':rows[4], 'price':rows[5]})
            for item in dict_list:
                sql = "INSERT INTO menu(m_id, menu_id, r_id, f_id, cuisine, price) VALUES (%s, %s, %s, %s, %s, %s)"
                val = item['m_id'], item['menu_id'], item['r_id'], item['f_id'], item['cuisine'], item['price']
                cursor.execute(sql, val)
                dict_list.clear()
            dict_list.clear()
            conn.commit()

    dict_list = list()
    with csv4.open(mode="r",encoding="utf-8") as csv_reader4:
        csv_reader4 = csv.reader(csv_reader4)
        next(csv_reader4)  # Skip the header row
        for rows in csv_reader4:
            dict_list.append({'user_id':rows[0], 'name':rows[1], 'age':rows[2],'gender':rows[3], 'marital_status':rows[4], 'occupation':rows[5],'usercity':rows[6]})
            for item in dict_list:
                sql = "INSERT INTO users(user_id, name, age, gender, marital_status, occupation, usercity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = item['user_id'], item['name'], item['age'], item['gender'], item['marital_status'], item['occupation'], item['usercity']
                cursor.execute(sql, val)
                dict_list.clear()
            dict_list.clear()
            conn.commit()

    dict_list = list()
    with csv5.open(mode="r",encoding="utf-8") as csv_reader5:
        csv_reader5 = csv.reader(csv_reader5)
        next(csv_reader5)  # Skip the header row
        for rows in csv_reader5:
            dict_list.append({ 'o_id':rows[0],
                               'order_date':rows[1],
                               'sales_qty':rows[2],
                               'sales_amount':rows[3], 
                               'currency':rows[4],
                               'user_id':rows[5], 
                               'r_id':rows[6] if rows[6].strip() != '' else None, 
                               'order_city':rows[7] if rows[7].strip() != '' else None})
            for item in dict_list:
                sql = "INSERT INTO orders(o_id, order_date, sales_qty, sales_amount, currency, user_id, r_id, order_city) VALUES (%s, %s, %s, %s, %s, %s, %s ,%s)"
                val = item['o_id'], item['order_date'], item['sales_qty'],item['sales_amount'], item['currency'], item['user_id'], item['r_id'], item['order_city']
                cursor.execute(sql, val)
                dict_list.clear()
            dict_list.clear()
            conn.commit()


def get_session():
    with Session(bind=engine,autocommit=False,autoflush=False) as db:
        yield db