from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called, have_been_called_with
from expects import expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import CreateUserCommandHandlerException, UsersRepositoryException
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from src.use_cases.commands.create_user_command import (
    CreateUserCommand,
    CreateUserCommandHandler,
)
from tests.test_data import TestData


class TestCreateUserCommandHandler:
    def test_create_user(self) -> None:
        user = TestData.a_user()
        session = Mimic(Spy, Session)
        command = CreateUserCommand(session, user)
        users_repository = Mimic(Spy, PostgresUsersRepository)
        handler = CreateUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.save).to(have_been_called_with(session, user))
        expect(session.commit).to(have_been_called)
        expect(session.close).to(have_been_called)
        expect(session.rollback).not_to(have_been_called)

    def test_raise_error_when_creating_a_user(self) -> None:
        user = TestData.a_user()
        error_message = "any error"
        session = Mimic(Spy, Session)
        command = CreateUserCommand(session, user)
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.save(ANY_ARG).raises(UsersRepositoryException(error_message))
        handler = CreateUserCommandHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(command)).to(raise_error(CreateUserCommandHandlerException, error_message))
        expect(session.rollback).to(have_been_called)
        expect(session.close).to(have_been_called)
        expect(session.commit).not_to(have_been_called)
