from http.client import CREATED

from fastapi import APIRouter, Depends

from src.delivery.api.v1.users.users_requests import UserRequest
from src.domain.user import User
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)

users_router = APIRouter()


def _get_create_users_command_handler() -> CreateUserCommandHandler:
    return CreateUserCommandHandler()


@users_router.post("/", status_code=CREATED)
def create_user(
    user_request: UserRequest,
    handler: CreateUserCommandHandler = Depends(_get_create_users_command_handler),
) -> None:
    user = User(**dict(user_request))
    command = CreateUserCommand(user)
    handler.execute(command)
