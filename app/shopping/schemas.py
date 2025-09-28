from pydantic import BaseModel, conlist

class ShoppingListIn(BaseModel):
    name: str
    recipe_ids: conlist(int, min_length=1) 


class ShoppingListOut(BaseModel):
    id: int
    name: str
