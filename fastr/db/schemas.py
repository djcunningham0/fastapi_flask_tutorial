from pydantic import BaseModel
from typing import Optional


### user schemas
class User(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreate(User):
    hashed_password: str


class LoggedInUser(User):
    id: int


### post schemas
class Post(BaseModel):
    title: str
    body: Optional[str] = None

    class Config:
        orm_mode = True


class PostUpdate(Post):
    id: int
