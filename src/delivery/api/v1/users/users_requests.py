from pydantic import BaseModel


class UserRequest(BaseModel):
    id: str
    name: str
    age: int


class UserUpdateRequest(BaseModel):
    name: str
    age: int
