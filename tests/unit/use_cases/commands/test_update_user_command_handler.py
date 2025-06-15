from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called, have_been_called_with
from expects import expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from src.use_cases.commands.update_user_command import (
    UpdateUserCommand,
    UpdateUserCommandHandler,
)
from tests.test_data import TestData


class TestUpdateUserCommandHandler:
    def test_update_user(self) -> None:
        user = TestData.a_user()
        session = Mimic(Spy, Session)
        command = UpdateUserCommand(session, user)
        users_repository = Mimic(Spy, PostgresUsersRepository)
        handler = UpdateUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.update).to(have_been_called_with(session, user))
        expect(session.commit).to(have_been_called)
        expect(session.close).to(have_been_called)
        expect(session.rollback).not_to(have_been_called)

    def test_raise_error_when_updating_a_non_existing(self) -> None:
        user = TestData.a_user()
        error_message = f"User with ID: '{user.id}' not found."
        session = Mimic(Spy, Session)
        command = UpdateUserCommand(session, user)
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.update(ANY_ARG).raises(NotFoundUsersRepositoryException(user.id))
        handler = UpdateUserCommandHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(command)).to(raise_error(NotFoundUserException, error_message))
        expect(session.rollback).to(have_been_called)
        expect(session.close).to(have_been_called)
        expect(session.commit).not_to(have_been_called)
