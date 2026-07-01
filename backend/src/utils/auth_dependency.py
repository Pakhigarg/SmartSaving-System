from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.security import decode_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    print("TOKEN:", token)

    user = decode_token(token)

    print("USER:", user)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return user