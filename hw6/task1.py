
# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из 
# трёх таблиц: товары, заказы и пользователи.
# — Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
# — Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
# — Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях
# магазина.

# • Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия,
# адрес электронной почты и пароль.
# • Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя 
# (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
# • Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой 
# из трёх таблиц.
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API.


import databases
import sqlalchemy
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime


DATABASE_URL = "sqlite:///shopdatabase.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32)),
    sqlalchemy.Column("price", sqlalchemy.Float),
    sqlalchemy.Column("description", sqlalchemy.String(100)),
)


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, foreign_key=True),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, foreign_key=True),
    sqlalchemy.Column("date", sqlalchemy.DateTime),
    sqlalchemy.Column("status", sqlalchemy.String(50))

)

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String(50)),
    sqlalchemy.Column("second_name", sqlalchemy.String(50)),
    sqlalchemy.Column("email", sqlalchemy.String(32)),
    sqlalchemy.Column("password", sqlalchemy.String(32)),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

class User(BaseModel):
    first_name: str = Field(max_length=50)
    second_name: str = Field(max_length=50)
    email: str = Field(max_length=32)
    password: str = Field(min_length=10)

class UserId(User):
    id: int

class Product(BaseModel):
    name: str = Field(max_length=32)
    price: float = Field(gt=0)
    description: str = Field(max_length=100)

class ProductId(Product):
    id: int

class Order(BaseModel):
    user_id: int
    product_id: int
    date: datetime
    status: str = Field(max_lenth=50)

class OrderId(User):
    id: int


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# маршрутизация для пользователя

@app.get("/fake_users/{count}")
async def create_users(count: int):
    for i in range(count):
        query = users.insert().values(first_name=f'user{i}',
        second_name=f'last{i}',                             
        email=f'mail{i}@mail.ru',
        password=f'password{i}')
        await database.execute(query)
    return {'message': f'{count} fake users created'}

@app.get("/users/", response_model=List[User])
async def get_users():
    query = users.select()
    return await database.fetch_all(query)

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)

@app.post("/users/", response_model=UserId)
async def create_user(user: User):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: User):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}

# маршруты для товаров

@app.get("/products/", response_model=List[Product])
async def get_products():
    query = products.select()
    return await database.fetch_all(query)

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)

@app.post("/products/", response_model=ProductId)
async def create_product(product: Product):
    query = products.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), "id": last_record_id}

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: Product):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {"message": "Product deleted"}

# маршруты для заказов

@app.get("/orders/", response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)

@app.post("/orders/", response_model=OrderId)
async def create_order(order: Order):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), "id": last_record_id}

@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: Order):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": "Order deleted"}

