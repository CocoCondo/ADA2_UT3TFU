from pydantic import BaseModel

class ProductIn(BaseModel):
    name: str
    unit: str

class ProductOut(ProductIn):
    id: int
