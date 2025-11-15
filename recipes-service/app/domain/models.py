from pydantic import BaseModel


class Recipe(BaseModel):
    id: int | None = None
    name: str
    steps: str | None = None


class RecipeCreate(BaseModel):
    name: str
    steps: str | None = None


class RecipeItem(BaseModel):
    recipe_id: int
    product_id: int
    qty: float


class RecipeItemCreate(BaseModel):
    product_id: int
    qty: float