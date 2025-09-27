from fastapi import APIRouter, Path
from .schemas import RecipeIn, RecipeOut, RecipeItemIn
from . import service

router = APIRouter()

@router.post("", response_model=dict)
def create_recipe(r: RecipeIn):
    return service.create_recipe(r)

@router.get("", response_model=list[RecipeOut])
def list_recipes():
    return service.get_all_recipes()

@router.post("/{recipe_id}/items", response_model=dict)
def add_item(
    recipe_id: int = Path(..., gt=0),
    item: RecipeItemIn = ...
):
    return service.add_recipe_item(recipe_id, item)
