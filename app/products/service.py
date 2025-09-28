from .schemas import ProductIn, ProductOut
from . import repo

def create_product(data: ProductIn) -> dict:
    new_id = repo.insert_product(data.model_dump())
    return {"id": new_id, "status": "created"}

def get_all_products() -> list[ProductOut]:
    return [ProductOut(**r) for r in repo.list_products()]
