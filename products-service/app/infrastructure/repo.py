from typing import List
from sqlalchemy import text
from app.infrastructure.db import get_connection
from app.domain.models import Product, ProductCreate


def insert_product(data: ProductCreate) -> int:
    sql = text("""
        INSERT INTO products (name, unit)
        VALUES (:name, :unit)
        RETURNING id
    """)
    with get_connection() as conn:
        res = conn.execute(sql, {"name": data.name, "unit": data.unit})
        new_id = res.scalar_one()
        conn.commit()
    return new_id


def list_products() -> List[Product]:
    sql = text("SELECT id, name, unit FROM products ORDER BY id")
    with get_connection() as conn:
        rows = conn.execute(sql).mappings().all()
    return [Product(**row) for row in rows]