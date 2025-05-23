from http.client import CREATED, NO_CONTENT, OK

import pytest
from doublex import Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import equal, expect
from fastapi.testclient import TestClient

from main import app
from src.delivery.api.v1.users.users_router import (
    _get_create_users_command_handler,
    _get_delete_one_user_command_handler,
    _get_find_all_users_query_handler,
    _get_find_one_user_query_handler,
    _get_update_one_user_command_handler,
)
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
    UpdateUserCommandResponse,
)
from src.use_cases.queries.find_all_users_query import (
    FindAllUsersQueryHandler,
    FindAllUsersQueryResponse,
)
from src.use_cases.queries.find_one_user_query import (
    FindOneUserQuery,
    FindOneUserQueryHandler,
    FindOneUserQueryResponse,
)
from tests.test_data import TestData


class TestUsersRouter:
    @pytest.fixture(autouse=True)
    def client(self) -> TestClient:
        return TestClient(app)

    def test_create_user(self, client: TestClient) -> None:
        user = TestData.a_user()
        payload = TestData.a_payload_from_a_user(user)
        handler = Mimic(Spy, CreateUserCommandHandler)
        app.dependency_overrides[_get_create_users_command_handler] = lambda: handler
        command = CreateUserCommand(user)

        response = client.post("/api/v1/users", json=payload)

        expect(response.status_code).to(equal(CREATED))
        expect(handler.execute).to(have_been_called_with(command))

    def test_find_all_users(self, client: TestClient) -> None:
        user = TestData.a_user()
        with Mimic(Stub, FindAllUsersQueryHandler) as handler:
            query_response = FindAllUsersQueryResponse([user])
            handler.execute().returns(query_response)
        app.dependency_overrides[_get_find_all_users_query_handler] = lambda: handler

        response = client.get("/api/v1/users")

        expect(response.status_code).to(equal(OK))
        expect(response.json()).to(equal({"users": [user.json()]}))

    def test_find_one_user(self, client: TestClient) -> None:
        user = TestData.a_user()
        with Mimic(Stub, FindOneUserQueryHandler) as handler:
            query_response = FindOneUserQueryResponse(user)
            query = FindOneUserQuery(user.id)
            handler.execute(query).returns(query_response)
        app.dependency_overrides[_get_find_one_user_query_handler] = lambda: handler

        response = client.get(f"/api/v1/users/{user.id.hex}")

        expect(response.status_code).to(equal(OK))
        expect(response.json()).to(equal(user.json()))

    def test_update_one_user(self, client: TestClient) -> None:
        user = TestData.a_user()
        user_id = user.id.hex
        payload = {"name": user.name, "age": user.age}
        with Mimic(Stub, UpdateUserCommandHandler) as handler:
            command_response = UpdateUserCommandResponse(user)
            command = UpdateUserCommand(user)
            handler.execute(command).returns(command_response)
        app.dependency_overrides[_get_update_one_user_command_handler] = lambda: handler

        response = client.put(f"/api/v1/users/{user_id}", json=payload)

        expect(response.status_code).to(equal(OK))
        expected_user = {"id": user.id.hex, "name": user.name, "age": user.age}
        expect(response.json()).to(equal(expected_user))

    def test_delete_one_user(self, client: TestClient) -> None:
        user_id = TestData.ANY_USER_ID
        command = DeleteUserCommand(user_id)
        _handler = Mimic(Spy, DeleteUserCommandHandler)

        def handler() -> DeleteUserCommandHandler:
            return _handler  # type: ignore

        app.dependency_overrides[_get_delete_one_user_command_handler] = handler

        response = client.delete(f"/api/v1/users/{user_id.hex}")

        expect(response.status_code).to(equal(NO_CONTENT))
        expect(_handler.execute).to(have_been_called_with(command))
