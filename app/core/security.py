"""Encryption related functions"""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

from .config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
EMAIL_TOKEN_EXPIRE_DAYS = 1


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_email_hash(email):
    return pwd_context.hash(email)


def verify_email(*, plain_email, hashed_email):
    return pwd_context.verify(plain_email, hashed_email)


def create_access_token(user_id: str):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": user_id}
    secret_key = get_settings().secret_key
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    secret_key = get_settings().secret_key
    payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
    return payload


def create_email_token(email: str):
    expires_delta = timedelta(days=EMAIL_TOKEN_EXPIRE_DAYS)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "email": email}
    secret_key = get_settings().secret_key
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_email_token(token: str):
    return decode_access_token(token)
