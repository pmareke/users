from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    name: str
    age: int


class UsersResponse(BaseModel):
    users: list[UserResponse]
