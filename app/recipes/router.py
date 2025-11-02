# app/recipes/router.py
from fastapi import APIRouter, Path, Depends
from .schemas import RecipeIn, RecipeOut, RecipeItemIn
from . import service, tasks
from app.security import RequireJWT
from .service import enqueue_recipe, queue_stats

router = APIRouter()
require_jwt = RequireJWT()

@router.post("", response_model=dict, dependencies=[Depends(require_jwt)])
def create_recipe(r: RecipeIn):
    return service.create_recipe(r)

@router.get("", response_model=list[RecipeOut], dependencies=[Depends(require_jwt)])
def list_recipes():
    return service.get_all_recipes()

@router.post("/{recipe_id}/items", response_model=dict, dependencies=[Depends(require_jwt)])
def add_item(
    recipe_id: int = Path(..., gt=0),
    item: RecipeItemIn = ...
):
    return service.add_recipe_item(recipe_id, item)

@router.post("/enqueue", dependencies=[Depends(require_jwt)], response_model=dict)
def enqueue(body: dict):
    return enqueue_recipe(body)

@router.get("/queue/stats", dependencies=[Depends(require_jwt)], response_model=dict)
def stats():
    return queue_stats()