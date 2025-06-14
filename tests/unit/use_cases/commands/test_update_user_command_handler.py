from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import expect, raise_error

from src.domain.exceptions import NotFoundUserException, NotFoundUserRepositoryException
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

    def test_raise_error_when_updating_a_non_existing(self) -> None:
        user = TestData.a_user()
        error_message = f"User with ID: '{user.id.hex}' not found."
        command = UpdateUserCommand(user)
        with Mimic(Stub, InMemoryUsersRepository) as users_repository:
            users_repository.update(ANY_ARG).raises(NotFoundUserRepositoryException(user.id))
        handler = UpdateUserCommandHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(command)).to(raise_error(NotFoundUserException, error_message))
