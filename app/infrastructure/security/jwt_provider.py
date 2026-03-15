from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class JwtProvider:  # <- IMPORTANT: même nom que ton import

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    def get_user_id(self, token: str) -> int:
        payload = self.decode(token)
        # tu choisis la clé : "sub" ou "user_id"
        if "sub" in payload:
            return int(payload["sub"])
        if "user_id" in payload:
            return int(payload["user_id"])
        raise ValueError("Token has no user id")