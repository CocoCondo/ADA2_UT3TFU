from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.security import issue_demo_jwt
from app.config import settings
import jwt as pyjwt

router = APIRouter()

class TokenReq(BaseModel):
    sub: str = "demo-user"
    extra: dict | None = None

@router.post("/demo-token", response_model=dict)
def demo_token(body: TokenReq):
    # Solo disponible si está habilitado en config
    if not settings.ENABLE_DEMO_TOKEN:
        raise HTTPException(404, "not found")
    token = issue_demo_jwt(body.sub, body.extra)
    # Devolvemos token y payload decodificado para mostrar en la demo
    payload = pyjwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=["RS256"], audience=settings.API_AUDIENCE, options={"verify_exp": True}, issuer=settings.JWT_ISSUER)
    return {"token": token, "payload": payload, "ttl_min": settings.JWT_TTL_MIN}
