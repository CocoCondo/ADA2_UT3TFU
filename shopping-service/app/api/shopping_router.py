from typing import List
from fastapi import APIRouter, Path
from app.domain.models import ShoppingList, ShoppingListCreate
from app.domain import services

router = APIRouter(prefix="/shopping-lists", tags=["shopping"])


@router.post("", response_model=dict)
def create_list(payload: ShoppingListCreate):
    new_id = services.create_shopping_list(payload)
    return {"id": new_id, "status": "created"}


@router.get("/{list_id}", response_model=dict)
def get_list(list_id: int = Path(..., gt=0)):
    data = services.get_shopping_list(list_id)
    if not data:
        return {"detail": "not found"}
    return data

@router.get("", response_model=List[ShoppingList])
def list_lists():
    return services.list_shopping_lists()