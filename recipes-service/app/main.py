from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.recipes_router import router as recipes_router
from app.api.recipes_soap_router import router as recipes_soap_router

app = FastAPI(title="Recipes Service")

# Origines permitidos (frontend Nginx)
origins = [
    "http://localhost:8090",
    # si después lo servís en otro host/puerto, lo agregás acá
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # GET, POST, OPTIONS, etc.
    allow_headers=["*"],   # Content-Type, Authorization, etc.
)

@app.get("/health", tags=["health"])
def health():
    return {"ok": True, "service": "recipes"}


app.include_router(recipes_router)
app.include_router(recipes_soap_router)