from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError

from app.db import tables
from ...dependencies import authenticate_user, get_current_user
from app.core.security import create_access_token, create_email_token, decode_email_token, get_password_hash
from app import models
from app.crud import user as db_user
from app.core.config import get_settings
from app.util.email_helper import send_reset_pw_link_email, is_valid_email, send_new_account_email


router = APIRouter()


class NewUser(BaseModel):
    id: int
    name: str
    email: str


class UserRegisterForm(BaseModel):
    email: str
    password: str
    username: str | None = None
    activation_link: str | None = None


class ForgetPwForm(BaseModel):
    email: str
    reset_link: str | None = None


class ResetPwForm(BaseModel):
    password: str


@router.post("/users/register", response_model=NewUser, status_code=status.HTTP_201_CREATED)
def create_user(form: UserRegisterForm):
    """
    Create new user based on unique email.
    """
    user_match = db_user.get_user_by_email(email=form.email)
    if user_match:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email already exists in the system.",
        )
    new_user = db_user.create_user(email=form.email, password=form.password)
    if get_settings().emails_enabled and form.email:
        token = create_email_token(form.email)
        # TODO use dynamic url creation
        root = get_settings().api_url
        activation_link = f"https://{root}/users/activation/?token={token}"
        send_new_account_email(form.email, activation_link)
        print("email sent to user")
    return NewUser(id=new_user.id, email=new_user.email, name=new_user.name)


@router.get("/users/activation")
def activate_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token."
    )
    try:
        payload = decode_email_token(token)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db_user.get_user_by_email(email=email)
    user.is_active = True
    user = db_user.update_user(user)
    return {"message": "Email validation OK."}


@router.post("/users/login", response_model=models.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """login with email (as username) and password"""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/forget-pw")
def get_reset_pw_link(form: ForgetPwForm):
    """Return an access token"""
    if not is_valid_email(form.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email format error")
    if db_user.get_user_by_email(form.email) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    token = create_access_token(form.email)
    if form.reset_link is None:
        root = get_settings().api_url
        reset_link = f"http://{root}/users/password/?token={token}"
    else:
        reset_link = form.reset_link

    send_reset_pw_link_email(form.email, reset_link)
    return {"token": token}


@router.put("/users/password")
def reset_pw(form: ResetPwForm, user: Annotated[tables.User, Depends(get_current_user)]):
    new_hashed_password = get_password_hash(form.password)
    user.password = new_hashed_password
    db_user.update_user(user)
    return {"message": "Password updated."}


@router.get("/users/test-token", response_model=models.User)
async def read_users_me(
    user: Annotated[tables.User, Depends(get_current_user)]
):
    return models.User(name=user.name, email=user.email, password=user.password, id=user.id, is_active=user.is_active)
