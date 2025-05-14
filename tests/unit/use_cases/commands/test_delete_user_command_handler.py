from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.commands.delete_user_command import (
    DeleteUserCommand,
    DeleteUserCommandHandler,
)
from tests.test_data import TestData


class TestDeleteUserCommandHandler:
    def test_delete_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        command = DeleteUserCommand(user_id)
        users_repository = Mimic(Spy, InMemoryUsersRepository)
        handler = DeleteUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.delete).to(have_been_called_with(user_id))
