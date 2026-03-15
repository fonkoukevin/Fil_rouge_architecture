from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.infrastructure.security.jwt_provider import JwtProvider

security = HTTPBearer()

def get_jwt_provider() -> JwtProvider:
    return JwtProvider()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    jwt_provider: JwtProvider = Depends(get_jwt_provider),
) -> int:
    token = credentials.credentials
    try:
        return jwt_provider.get_user_id(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")