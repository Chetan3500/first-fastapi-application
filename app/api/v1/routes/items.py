"""Contains the CRUD endpoints for items, using the databases library for async queries."""

from fastapi import APIRouter, HTTPException
from databases import Database
from app.models.item import Item
from app.core.config import settings

router = APIRouter()
database = Database(settings.DATABASE_URL)


@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    """CREATE ITEM"""
    query = "INSERT INTO items (id, name, price, is_available) VALUES (:id, :name, :price, :is_available) RETURNING *"
    values = {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "is_available": item.is_available,
    }
    result = await database.fetch_one(query=query, values=values)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to create item")
    return item


@router.get("/items/", response_model=list[Item])
async def read_items():
    """READ ALL ITEM"""
    query = "SELECT * FROM items"
    return await database.fetch_all(query=query)


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """READ SPECIFIC ITEM VIA ID"""
    query = "SELECT * FROM items WHERE id = :id"
    result = await database.fetch_one(query=query, values={"id": item_id})
    if result is None:
        raise HTTPException(status_code=400, detail="Item not found")
    return result


@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    """UPDATE SPECIFIC ITEM VIA ID"""
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
        raise HTTPException(status_code=400, detail="Item not found")
    return result


@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """DELETE SPECIFIC ITEM VIA ID"""
    query = "DELETE FROM items WHERE id = :id RETURNING *"
    result = await database.fetch_one(query=query, values={"id": item_id})
    if result is None:
        raise HTTPException(status_code=400, detail="Item not found")
    return {"message": "Item deleted"}
