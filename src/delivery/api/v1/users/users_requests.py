from uuid import UUID

from pydantic import BaseModel


class UserRequest(BaseModel):
    id: UUID
    name: str
    age: int


class UserUpdateRequest(BaseModel):
    name: str
    age: int
