from fastapi import APIRouter, Path
from .schemas import ShoppingListIn
from . import service

router = APIRouter()

@router.post("", response_model=dict)
def create_list(body: ShoppingListIn):
    return service.create_from_recipes(body)

@router.get("/{list_id}", response_model=dict)
def get_list(list_id: int = Path(..., gt=0)):
    return service.get_list_detail(list_id)
