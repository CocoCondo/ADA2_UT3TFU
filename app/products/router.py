# app/products/router.py
from fastapi import APIRouter
from .schemas import ProductIn, ProductsResponse
from . import service

router = APIRouter()

@router.get("", response_model=ProductsResponse)
def list_products():
    return service.get_all_products()

@router.post("", response_model=dict)
def add_product(p: ProductIn):
    return service.create_product(p)
