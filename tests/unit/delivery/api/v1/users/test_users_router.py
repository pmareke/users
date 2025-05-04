from http.client import CREATED

import pytest
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
