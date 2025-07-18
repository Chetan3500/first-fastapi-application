# The entry point for the FastAPI application, initializing the app and including API routes.

from fastapi import FastAPI
from app.api.v1.routes import items
from app.core.database import engine, Base
from app.core.config import settings

app = FastAPI(title="FastAPI PostgreSQL CRUD", version="1.0.0")

# Create database tables on startup
@app.on_event("startup")
async def startup():
    await items.database.connect()
    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await items.database.disconnect()

# Include API routes
app.include_router(items.router, prefix="/api/v1", tags=["items"])

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
