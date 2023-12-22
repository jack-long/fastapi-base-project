from typing import Annotated

from fastapi import APIRouter, Depends
from app.api.dependencies import oauth2_scheme

router = APIRouter()


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
