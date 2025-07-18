# Define the Pydantic model for request/respond validation

from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool = True

    class Config:
        from_attributes = True