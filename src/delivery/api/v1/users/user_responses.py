from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    name: str
    age: int


class UsersResponse(BaseModel):
    users: list[UserResponse]
