# Building a CRUD API

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool = True

# In-memory storage (replace with a database in production)
items_db = []

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    if any(existing_item.id == item.id for existing_item in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(index)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

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