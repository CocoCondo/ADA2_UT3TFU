from pydantic import BaseModel

class ProductIn(BaseModel):
    name: str
    unit: str

class ProductOut(ProductIn):
    id: int
    class Config:
        orm_mode = True

class RecipeIn(BaseModel):
    name: str
    steps: str | None = None

class RecipeOut(RecipeIn):
    id: int
    class Config:
        orm_mode = True
