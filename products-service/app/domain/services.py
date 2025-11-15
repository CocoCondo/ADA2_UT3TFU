from typing import List
from app.domain.models import Product, ProductCreate
from app.infrastructure import repo


def create_product(data: ProductCreate) -> Product:
    new_id = repo.insert_product(data)
    return Product(id=new_id, name=data.name, unit=data.unit)


def get_all_products() -> List[Product]:
    return repo.list_products()