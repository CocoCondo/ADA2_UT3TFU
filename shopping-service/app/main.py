from fastapi import FastAPI
from app.api.shopping_router import router as shopping_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Shopping Service")

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
    return {"ok": True, "service": "shopping"}


app.include_router(shopping_router)