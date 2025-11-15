from typing import List
from fastapi import APIRouter, Path
from app.domain.models import Recipe, RecipeCreate, RecipeItemCreate
from app.domain import services

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.post("", response_model=Recipe)
def create_recipe(payload: RecipeCreate):
    return services.create_recipe(payload)


@router.get("", response_model=List[Recipe])
def list_recipes():
    return services.get_all_recipes()


@router.post("/{recipe_id}/items", response_model=dict)
def add_item(
    recipe_id: int = Path(..., gt=0),
    item: RecipeItemCreate = ...
):
    services.add_item(recipe_id, item)
    return {"status": "ok"}