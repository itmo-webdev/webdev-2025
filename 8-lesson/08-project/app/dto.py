from pydantic import BaseModel


class ScrappedUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str


class User(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
