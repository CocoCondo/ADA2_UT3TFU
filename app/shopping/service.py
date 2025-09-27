from fastapi import HTTPException
from .schemas import ShoppingListIn, ShoppingListOut
from . import repo

def create_from_recipes(data: ShoppingListIn) -> dict:
    if not data.recipe_ids:
        raise HTTPException(400, "Debes enviar al menos una receta.")

    list_id = repo.create_list(data.name)
    totals = repo.items_from_recipes(data.recipe_ids)

    for row in totals:
        repo.upsert_item(list_id, row["product_id"], row["qty"])

    return {"id": list_id, "status": "created"}

def get_list_detail(list_id: int) -> dict:
    res = repo.get_list(list_id)
    if not res["list"]:
        raise HTTPException(404, "Lista no encontrada")
    return res
