from http.client import CREATED

from fastapi import APIRouter

from src.delivery.api.v1.users.users_requests import UserRequest

users_router = APIRouter()


@users_router.post("/", status_code=CREATED)
def create_user(user_request: UserRequest) -> None:
    pass
