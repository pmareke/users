from http.client import CREATED

from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import equal, expect
from fastapi.testclient import TestClient

from main import app
from src.delivery.api.v1.users.users_router import _get_create_users_command_handler
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from tests.test_data import TestData


class TestUsersRouter:
    def test_create_user(self) -> None:
        user = TestData.a_user()
        payload = TestData.a_payload_from_user(user)
        command = CreateUserCommand(user)
        client = TestClient(app)
        handler = Mimic(Spy, CreateUserCommandHandler)

        app.dependency_overrides[_get_create_users_command_handler] = lambda: handler

        response = client.post("/api/v1/users", json=payload)

        expect(response.status_code).to(equal(CREATED))
        expect(handler.execute).to(have_been_called_with(command))
