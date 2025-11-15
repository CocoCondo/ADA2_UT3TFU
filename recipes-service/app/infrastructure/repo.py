from typing import List
from sqlalchemy import text
from app.infrastructure.db import get_connection
from app.domain.models import Recipe, RecipeCreate, RecipeItemCreate


def insert_recipe(data: RecipeCreate) -> int:
    sql = text("""
        INSERT INTO recipes (name, steps)
        VALUES (:name, :steps)
        RETURNING id
    """)
    with get_connection() as conn:
        res = conn.execute(sql, {"name": data.name, "steps": data.steps})
        rid = res.scalar_one()
        conn.commit()
    return rid


def list_recipes() -> List[Recipe]:
    sql = text("SELECT id, name, steps FROM recipes ORDER BY id")
    with get_connection() as conn:
        rows = conn.execute(sql).mappings().all()
    return [Recipe(**row) for row in rows]


def add_recipe_item(recipe_id: int, item: RecipeItemCreate) -> None:
    sql = text("""
        INSERT INTO recipe_items (recipe_id, product_id, qty)
        VALUES (:r, :p, :q)
        ON CONFLICT (recipe_id, product_id)
        DO UPDATE SET qty = EXCLUDED.qty
    """)
    with get_connection() as conn:
        conn.execute(sql, {"r": recipe_id, "p": item.product_id, "q": item.qty})
        conn.commit()