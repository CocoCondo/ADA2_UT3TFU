# app/products/schemas.py
from pydantic import BaseModel
from typing import Literal, List

class ProductIn(BaseModel):
    name: str
    unit: str

class ProductOut(BaseModel):
    id: int
    name: str
    unit: str

class ProductsResponse(BaseModel):
    source: Literal["db", "cache"]
    items: List[ProductOut]
