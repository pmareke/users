from http.client import CREATED, INTERNAL_SERVER_ERROR, NO_CONTENT, NOT_FOUND, OK
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.delivery.api.v1.users.user_responses import UserResponse, UsersResponse
from src.delivery.api.v1.users.users_requests import UserRequest, UserUpdateRequest
from src.domain.exceptions import (
    CreateUserCommandHandlerException,
    FindAllUsersQueryHandlerException,
    NotFoundUserException,
)
from src.domain.user import User
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from src.use_cases.commands.delete_user_command import (
    DeleteUserCommand,
    DeleteUserCommandHandler,
)
from src.use_cases.commands.update_user_command import (
    UpdateUserCommand,
    UpdateUserCommandHandler,
)
from src.use_cases.queries.find_all_users_query import FindAllUsersQueryHandler
from src.use_cases.queries.find_one_user_query import (
    FindOneUserQuery,
    FindOneUserQueryHandler,
)

users_router = APIRouter()
users_repository = InMemoryUsersRepository()


def _get_create_users_command_handler() -> CreateUserCommandHandler:
    return CreateUserCommandHandler(users_repository)


def _get_find_all_users_query_handler() -> FindAllUsersQueryHandler:
    return FindAllUsersQueryHandler(users_repository)


def _get_find_one_user_query_handler() -> FindOneUserQueryHandler:
    return FindOneUserQueryHandler(users_repository)


def _get_update_one_user_command_handler() -> UpdateUserCommandHandler:
    return UpdateUserCommandHandler(users_repository)


def _get_delete_one_user_command_handler() -> DeleteUserCommandHandler:
    return DeleteUserCommandHandler(users_repository)


@users_router.post("/", status_code=CREATED)
def create_user(
    user_request: UserRequest,
    handler: CreateUserCommandHandler = Depends(_get_create_users_command_handler),
) -> None:
    try:
        user = _create_user_from_request(user_request)
        command = CreateUserCommand(user)
        handler.execute(command)
    except CreateUserCommandHandlerException as ex:
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"{ex}") from ex


@users_router.get("/", status_code=OK)
def find_all_users(
    handler: FindAllUsersQueryHandler = Depends(_get_find_all_users_query_handler),
) -> UsersResponse:
    try:
        response = handler.execute()
        users: list[UserResponse] = []
        for user in response.data():
            json_user = _build_user_response(user)
            users.append(json_user)
        return UsersResponse(users=users)
    except FindAllUsersQueryHandlerException as ex:
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=f"{ex}") from ex


@users_router.get("/{user_id}", status_code=OK)
def find_one_user(
    user_id: UUID,
    handler: FindOneUserQueryHandler = Depends(_get_find_one_user_query_handler),
) -> UserResponse:
    try:
        query = FindOneUserQuery(user_id)
        response = handler.execute(query)
        user = response.data()
        return _build_user_response(user)
    except NotFoundUserException as ex:
        raise HTTPException(status_code=NOT_FOUND, detail=f"{ex}") from ex


@users_router.put("/{user_id}", status_code=OK)
def update_user(
    user_id: UUID,
    user_request: UserUpdateRequest,
    handler: UpdateUserCommandHandler = Depends(_get_update_one_user_command_handler),
) -> UserResponse:
    try:
        user = User(user_id, user_request.name, user_request.age)
        command = UpdateUserCommand(user)
        response = handler.execute(command)
        user_response = response.data()
        return _build_user_response(user_response)
    except NotFoundUserException as ex:
        raise HTTPException(status_code=NOT_FOUND, detail=f"{ex}") from ex


@users_router.delete("/{user_id}", status_code=NO_CONTENT)
def delete_user(
    user_id: UUID,
    handler: DeleteUserCommandHandler = Depends(_get_delete_one_user_command_handler),
) -> None:
    try:
        command = DeleteUserCommand(user_id)
        handler.execute(command)
    except NotFoundUserException as ex:
        raise HTTPException(status_code=NOT_FOUND, detail=f"{ex}") from ex


def _create_user_from_request(user_request: UserRequest) -> User:
    return User(id=user_request.id, name=user_request.name, age=user_request.age)


def _build_user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, name=user.name, age=user.age)
