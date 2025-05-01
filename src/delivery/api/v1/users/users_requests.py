from pydantic import BaseModel


class UserRequest(BaseModel):
    id: str
    name: str
    age: int
