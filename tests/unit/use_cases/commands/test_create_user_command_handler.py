from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called_with
from expects import expect, raise_error

from src.domain.exceptions import CreateUserCommandHandlerException, UsersRepositoryException
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from tests.test_data import TestData


class TestCreateUserCommandHandler:
    def test_create_user(self) -> None:
        user = TestData.a_user()
        command = CreateUserCommand(user)
        users_repository = Mimic(Spy, InMemoryUsersRepository)
        handler = CreateUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.save).to(have_been_called_with(user))

    def test_raise_error_when_creating_a_user(self) -> None:
        user = TestData.a_user()
        error_message = "any error"
        command = CreateUserCommand(user)
        with Mimic(Stub, InMemoryUsersRepository) as users_repository:
            users_repository.save(ANY_ARG).raises(UsersRepositoryException(error_message))
        handler = CreateUserCommandHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(command)).to(raise_error(CreateUserCommandHandlerException, error_message))
