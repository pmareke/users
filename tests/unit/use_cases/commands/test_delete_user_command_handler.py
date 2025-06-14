from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import expect, raise_error

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
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

    def test_raise_error_when_deleting_a_non_existing_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        error_message = f"User with ID: '{user_id.hex}' not found."
        command = DeleteUserCommand(user_id)
        with Mimic(Stub, InMemoryUsersRepository) as users_repository:
            users_repository.delete(ANY_ARG).raises(NotFoundUsersRepositoryException(user_id))
        handler = DeleteUserCommandHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(command)).to(raise_error(NotFoundUserException, error_message))
