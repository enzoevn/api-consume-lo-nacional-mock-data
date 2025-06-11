from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserAuth(BaseModel):
    email: str
    password: str


class UserCreate(UserAuth):
    nick_name: str
    role: str
    image: str | None = None
