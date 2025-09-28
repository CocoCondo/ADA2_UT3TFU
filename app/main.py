from fastapi import FastAPI
from app.products import router as products_router
from app.recipes import router as recipes_router
from app.shopping import router as shopping_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.get("/health")  # health genérico del servicio
def health(): return {"ok": True}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(recipes_router,  prefix="/recipes",  tags=["recipes"])
app.include_router(shopping_router, prefix="/shopping-lists", tags=["shopping"])
