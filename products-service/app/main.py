from fastapi import FastAPI
from app.api.products_router import router as products_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Products Service")

origins = ["http://localhost:8090"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
def health():
    return {"ok": True, "service": "products"}


app.include_router(products_router)