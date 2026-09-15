from typing import Optional

from fastapi import Header, HTTPException

from services.firebase_service import verify_firebase_token


async def get_current_user(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format.")
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Authentication token is missing.")
    return verify_firebase_token(token)


async def get_optional_user(
    authorization: Optional[str] = Header(default=None),
) -> Optional[dict]:
    """Allow GRAMAI demo requests without auth while verifying supplied tokens."""
    if not authorization:
        return None
    return await get_current_user(authorization)