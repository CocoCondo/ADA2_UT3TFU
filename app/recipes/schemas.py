from pydantic import BaseModel, condecimal

class RecipeIn(BaseModel):
    name: str
    steps: str | None = None

class RecipeOut(RecipeIn):
    id: int

class RecipeItemIn(BaseModel):
    product_id: int
    qty: condecimal(gt=0)
