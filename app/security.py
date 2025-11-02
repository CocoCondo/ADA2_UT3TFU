from datetime import datetime, timedelta, timezone
from fastapi import Header, HTTPException
from app.config import settings
import jwt  # pyjwt

ALG = "RS256"

class RequireJWT:
    def __call__(self, authorization: str = Header(..., alias="Authorization")):
        try:
            token = authorization.split()[1]
            payload = jwt.decode(
                token,
                settings.JWT_PUBLIC_KEY,
                algorithms=[ALG],
                audience=settings.API_AUDIENCE,
                options={"verify_exp": True, "require": ["exp", "aud"]},
                issuer=settings.JWT_ISSUER if settings.JWT_ISSUER else None,
            )
            return payload
        except Exception:
            raise HTTPException(status_code=401, detail="invalid or missing token")

def issue_demo_jwt(sub: str, extra: dict | None = None) -> str:
    """SOLO para demo: firma un JWT RS256 con la private key."""
    if not settings.ENABLE_DEMO_TOKEN or not settings.JWT_PRIVATE_KEY:
        raise HTTPException(404, "token issuer disabled")
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.JWT_TTL_MIN)
    payload = {"sub": sub, "aud": settings.API_AUDIENCE, "iss": settings.JWT_ISSUER, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=ALG)
