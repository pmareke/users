from http.client import CREATED, OK
from uuid import UUID

from fastapi import APIRouter, Depends

from src.delivery.api.v1.users.user_responses import UserResponse, UsersResponse
from src.delivery.api.v1.users.users_requests import UserRequest
from src.domain.user import User
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from src.use_cases.queries.find_all_users_query import FindAllUsersQueryHandler

users_router = APIRouter()
users_repository = InMemoryUsersRepository()


def _get_create_users_command_handler() -> CreateUserCommandHandler:
    return CreateUserCommandHandler(users_repository)


def _get_find_all_users_query_handler() -> FindAllUsersQueryHandler:
    return FindAllUsersQueryHandler()


@users_router.post("/", status_code=CREATED)
def create_user(
    user_request: UserRequest,
    handler: CreateUserCommandHandler = Depends(_get_create_users_command_handler),
) -> None:
    user = _create_user_from_request(user_request)
    command = CreateUserCommand(user)
    handler.execute(command)


@users_router.get("/", status_code=OK)
def find_all_users(
    handler: FindAllUsersQueryHandler = Depends(_get_find_all_users_query_handler),
) -> UsersResponse:
    response = handler.execute()
    users: list[UserResponse] = []
    for user in response.data():
        json_user = UserResponse(id=user.id, name=user.name, age=user.age)
        users.append(json_user)
    return UsersResponse(users=users)


def _create_user_from_request(user_request: UserRequest) -> User:
    return User(
        id=UUID(user_request.id),
        name=user_request.name,
        age=user_request.age,
    )
