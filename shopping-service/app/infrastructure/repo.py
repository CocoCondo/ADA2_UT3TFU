from typing import List
from sqlalchemy import text
from app.infrastructure.db import get_connection
from app.domain.models import ShoppingList, ShoppingListCreate


def list_shopping_lists() -> List[ShoppingList]:
    sql = text("SELECT id, name FROM shopping_lists ORDER BY id")
    with get_connection() as conn:
        rows = conn.execute(sql).mappings().all()
    return [ShoppingList(**row) for row in rows]


def create_list(data: ShoppingListCreate) -> int:
    with get_connection() as conn:
        res = conn.execute(
            text("INSERT INTO shopping_lists (name) VALUES (:name) RETURNING id"),
            {"name": data.name},
        )
        list_id = res.scalar_one()

        # ejemplo simple: solo guarda receta_ids como texto o en tabla aparte
        for rid in data.recipe_ids:
            conn.execute(
                text("""
                    INSERT INTO shopping_list_recipes (list_id, recipe_id)
                    VALUES (:l, :r)
                """),
                {"l": list_id, "r": rid},
            )

        conn.commit()
    return list_id


def get_list(list_id: int) -> dict:
    with get_connection() as conn:
        head = conn.execute(
            text("SELECT id, name FROM shopping_lists WHERE id = :id"),
            {"id": list_id},
        ).mappings().first()

        if not head:
            return {}

        recipes = conn.execute(
            text("""
                SELECT recipe_id
                FROM shopping_list_recipes
                WHERE list_id = :id
            """),
            {"id": list_id},
        ).mappings().all()

    return {
        "id": head["id"],
        "name": head["name"],
        "recipes": [r["recipe_id"] for r in recipes],
    }