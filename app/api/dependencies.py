
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from ..models import User
from ..db import tables
from ..core.security import decode_access_token, verify_password
from ..crud import user as db_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


def authenticate_user(email: str, password: str):
    user = find_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def find_user_by_email(email: str) -> tables.User:
    if user := db_user.get_user_by_email(email=email):
        return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> tables.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = find_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
