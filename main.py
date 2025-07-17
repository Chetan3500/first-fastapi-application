# Building a CRUD API using PostgreSQL as the database.

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Database Setup
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://username:password@localhost:5432/fastapi_db"
)
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Model
class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    is_available = Column(Boolean, default=True)


# Pydantic Model
class Item(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool = True

    class Config:
        orm_mode = True


# Create database tables
Base.metadata.create_all(bind=engine)


# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# CRUD Endpoints
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    query = "INSERT INTO items (id, name, price, is_available) VALUES (:id, :name, :price, :is_available) RETURNING *"
    values = {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "is_available": item.is_available,
    }
    result = await database.fetch_one(query=query, values=values)
    if not result:
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    return item


@app.get("/items/", response_model=List[Item])
async def read_items():
    query = "SELECT * FROM items"
    return await database.fetch_all(query=query)


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    query = "SELECT * FROM items WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": item_id})
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    query = """
        UPDATE items
        SET name = :name, price = :price, is_available = :is_available
        WHERE id = :id
        RETURNING *
    """
    values = {
        "id": item_id,
        "name": updated_item.name,
        "price": updated_item.price,
        "is_available": updated_item.is_available,
    }
    result = await database.fetch_one(query=query, values=values)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    query = "DELETE FROM items WHERE id = :id RETURNING *"
    result = await database.fetch_one(query=query, values={"id": item_id})
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


################ BASIC AND CORE CONCEPT ################
# from fastapi import FastAPI # Import FastAPI class

# app = FastAPI() # Create an instance

# # hello from fastapi
# @app.get("/") # define a GET endpoint at the root url (/)
# async def root(): # handle requests to that endpoint
#     return {"message": "Hello, FastAPI!"} # sending a JSON response with message.

# # Core FastAPI Concept

# # 1. Path Parameters
# # Visit http://127.0.0.1:8000/items/42 to see: {"item_id": 42}.
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}

# # 2. Query Parameter
# # Query parameters are added to the URL after a ?, like ?name=Alice&category=books
# @app.get("/items/")
# async def read_items(name: str | None = None, category: str | None = None):
#     # None and = None make parameter optional
#     return {"name": name, "category": category}
# # Try http://127.0.0.1:8000/items/?name=Book&category=Stationery

# # 3. Request Body with Pydantic
# # to handle JSON data in POST requests using Pydantic models
# from pydantic import BaseModel
# class Item(BaseModel):
#     name: str
#     price: float
#     is_available: bool = True
# # Use /docs to send a POST request with JSON
# @app.post("/items/")
# async def create_item(item: Item):
#     return {"item": item.dict(), "message": "Item created"}

# # 4. Async vs Sync
# # For CPU-bound tasks, use def
# @app.get("/sync-example")
# def sync_example():
#     return {"message": "This is synchronous"}
# # FastAPI supports asynchronous programming with async def. Use it for I/O-bound tasks (e.g., database calls, API requests).
# @app.get("/async-example")
# async def async_example():
#     return {"message": "This is asynchronous"}
