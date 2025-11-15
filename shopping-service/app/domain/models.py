from pydantic import BaseModel
from typing import List


class ShoppingList(BaseModel):
    id: int | None = None
    name: str


class ShoppingListCreate(BaseModel):
    name: str
    recipe_ids: List[int]