from uuid import uuid4

from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.domain.user import User
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)


class TestCreateUserCommandHandler:
    def test_create_user_command_handler(self) -> None:
        user_id = uuid4()
        user = User(id=user_id, name="Peter", age=42)
        command = CreateUserCommand(user)
        users_repository = Mimic(Spy, InMemoryUsersRepository)
        handler = CreateUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.save).to(have_been_called_with(user))
