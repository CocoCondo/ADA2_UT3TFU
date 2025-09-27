from sqlalchemy import text
from app.db import engine

def insert_product(p: dict) -> int:
    with engine.begin() as c:
        return c.execute(
            text("""INSERT INTO products(name, unit) VALUES (:n,:u)
                    ON CONFLICT (name) DO UPDATE SET unit=EXCLUDED.unit
                    RETURNING id"""),
            {"n": p["name"], "u": p["unit"]}
        ).scalar()

def list_products() -> list[dict]:
    with engine.connect() as c:
        rows = c.execute(text("SELECT id,name,unit FROM products ORDER BY id")).mappings().all()
    return list(rows)
