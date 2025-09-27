from fastapi import HTTPException
from .schemas import RecipeIn, RecipeOut, RecipeItemIn
from . import repo

def create_recipe(data: RecipeIn) -> dict:
    rid = repo.insert_recipe(data.model_dict())
    return {"id": rid, "status": "created"}

def get_all_recipes() -> list[RecipeOut]:
    return [RecipeOut(**r) for r in repo.list_recipes()]

def add_recipe_item(recipe_id: int, item: RecipeItemIn):
    # Reglas mínimas (p.ej., qty > 0 ya lo valida Pydantic)
    try:
        repo.add_item(recipe_id, item.product_id, item.qty)
    except Exception as e:
        raise HTTPException(400, f"No se pudo agregar ingrediente: {e}")
    return {"status": "ok"}
