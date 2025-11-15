from pydantic import BaseModel

class Product(BaseModel):
    id: int | None = None
    name: str
    unit: str
    
class ProductCreate(BaseModel):
    name: str
    unit: str