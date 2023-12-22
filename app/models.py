from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    """Access token"""
    access_token: str
    token_type: str


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemInDB(ItemBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    name: str
    email: str


class User(UserBase):
    id: int
    full_name: str | None = None
    disabled: bool | None = None
    password: str
    is_active: bool
    items: list[ItemInDB] = []

    model_config = ConfigDict(from_attributes=True)
