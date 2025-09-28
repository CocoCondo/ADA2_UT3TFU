from sqlalchemy import text, bindparam
from app.db import engine

def create_list(name: str) -> int:
    with engine.begin() as c:
        return c.execute(
            text("INSERT INTO shopping_lists(name) VALUES (:n) RETURNING id"),
            {"n": name}
        ).scalar()

def upsert_item(list_id: int, product_id: int, qty) -> None:
    with engine.begin() as c:
        c.execute(
            text("""
                INSERT INTO shopping_list_items(list_id, product_id, qty)
                VALUES (:l,:p,:q)
                ON CONFLICT (list_id,product_id)
                DO UPDATE SET qty = shopping_list_items.qty + EXCLUDED.qty
            """),
            {"l": list_id, "p": product_id, "q": qty}
        )

def items_from_recipes(recipe_ids: list[int]) -> list[dict]:
    # usar IN :ids con expanding=True
    q = text("""
        SELECT ri.product_id, SUM(ri.qty) AS qty
        FROM recipe_items ri
        WHERE ri.recipe_id IN :ids
        GROUP BY ri.product_id
    """).bindparams(bindparam("ids", expanding=True))

    with engine.connect() as c:
        return list(c.execute(q, {"ids": recipe_ids}).mappings().all())

def get_list(list_id: int) -> dict | None:
    with engine.connect() as c:
        header = c.execute(
            text("SELECT id, name FROM shopping_lists WHERE id = :i"),
            {"i": list_id}
        ).mappings().first()
        if not header:
            return None
        # casteo qty a float desde SQL para evitar Decimal
        items = c.execute(
            text("""
                SELECT sli.product_id,
                       p.name,
                       (sli.qty)::float AS qty,
                       p.unit
                FROM shopping_list_items sli
                JOIN products p ON p.id = sli.product_id
                WHERE sli.list_id = :i
                ORDER BY p.name
            """),
            {"i": list_id}
        ).mappings().all()
    return {"list": dict(header), "items": [dict(r) for r in items]}
