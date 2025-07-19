"""Define the Pydantic model for request/respond validation"""

from pydantic import BaseModel


class Item(BaseModel):
    """Model"""

    id: int
    name: str
    price: float
    is_available: bool = True

    class Config:
        """Model Config"""

        from_attributes = True
