from fastapi import APIRouter
from .schemas import ProductIn, ProductOut
from . import service

router = APIRouter()

@router.post("", response_model=dict)
def create_product(p: ProductIn):
    return service.create_product(p)

@router.get("", response_model=list[ProductOut])
def list_products():
    return service.get_all_products()
