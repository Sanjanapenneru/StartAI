import json
import os
from functools import lru_cache

from fastapi import HTTPException


def _firebase_credentials():
    raw_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
    if raw_json:
        from firebase_admin import credentials
        return credentials.Certificate(json.loads(raw_json))

    path = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH")
    if path:
        from firebase_admin import credentials
        return credentials.Certificate(path)

    raise RuntimeError(
        "Firebase Admin is not configured. Set FIREBASE_SERVICE_ACCOUNT_JSON "
        "or FIREBASE_SERVICE_ACCOUNT_PATH."
    )


@lru_cache(maxsize=1)
def _initialize_firebase():
    import firebase_admin
    from firebase_admin import get_app

    try:
        return get_app()
    except ValueError:
        return firebase_admin.initialize_app(_firebase_credentials())


def verify_firebase_token(token: str) -> dict:
    try:
        _initialize_firebase()
        from firebase_admin import auth
        decoded_token = auth.verify_id_token(token)
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email", ""),
            "name": decoded_token.get("name", ""),
        }
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail="Authentication is not configured on this server.",
        ) from exc
    except Exception as exc:
        from firebase_admin import auth
        if isinstance(exc, auth.ExpiredIdTokenError):
            detail = "Token has expired. Please sign in again."
        elif isinstance(exc, auth.InvalidIdTokenError):
            detail = "Invalid authentication token."
        else:
            detail = "Authentication failed."
        raise HTTPException(status_code=401, detail=detail) from exc