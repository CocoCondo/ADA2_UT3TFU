from fastapi import APIRouter
from typing import List
from app.domain.models import Product, ProductCreate
from app.domain import services

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=Product)
def create_product(payload: ProductCreate):
    return services.create_product(payload)


@router.get("", response_model=List[Product])
def list_products():
    return services.get_all_products()