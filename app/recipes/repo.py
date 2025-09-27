from sqlalchemy import text
from app.db import engine

def insert_recipe(data: dict) -> int:
    with engine.begin() as c:
        return c.execute(
            text("INSERT INTO recipes(name, steps) VALUES (:n,:s) RETURNING id"),
            {"n": data["name"], "s": data.get("steps")}
        ).scalar()

def list_recipes() -> list[dict]:
    with engine.connect() as c:
        rows = c.execute(text("SELECT id,name,steps FROM recipes ORDER BY id")).mappings().all()
    return list(rows)

def add_item(recipe_id: int, product_id: int, qty) -> None:
    with engine.begin() as c:
        c.execute(
            text("""INSERT INTO recipe_items(recipe_id, product_id, qty)
                    VALUES (:r,:p,:q)
                    ON CONFLICT (recipe_id,product_id)
                    DO UPDATE SET qty = EXCLUDED.qty"""),
            {"r": recipe_id, "p": product_id, "q": qty}
        )
