from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.commands.update_user_command import (
    UpdateUserCommand,
    UpdateUserCommandHandler,
)
from tests.test_data import TestData


class TestUpdateUserCommandHandler:
    def test_update_user(self) -> None:
        user = TestData.a_user()
        command = UpdateUserCommand(user)
        users_repository = Mimic(Spy, InMemoryUsersRepository)
        handler = UpdateUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.update).to(have_been_called_with(user))
