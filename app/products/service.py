# app/products/service.py
import json
from .schemas import ProductIn, ProductOut
from . import repo
from app.cache import cache_get, cache_setex, cache_del

_CACHE_KEY = "products:all"
_TTL = 10  # segundos

def create_product(data: ProductIn) -> dict:
    new_id = repo.insert_product(data.model_dump())
    cache_del(_CACHE_KEY)  # invalidar caché distribuido
    return {"id": new_id, "status": "created"}

def get_all_products() -> dict:
    raw = cache_get(_CACHE_KEY)
    if raw:
        arr = json.loads(raw)  # list[dict]
        items = [ProductOut(**x) for x in arr]
        return {"source": "cache", "items": items}

    rows = repo.list_products()
    items = [ProductOut(**r) for r in rows]
    # guardamos en Redis como JSON plano
    cache_setex(_CACHE_KEY, _TTL, json.dumps([i.model_dump() for i in items]))
    return {"source": "db", "items": items}
