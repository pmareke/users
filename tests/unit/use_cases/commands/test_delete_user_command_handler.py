from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called, have_been_called_with
from expects import expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from src.use_cases.commands.delete_user_command import (
    DeleteUserCommand,
    DeleteUserCommandHandler,
)
from tests.test_data import TestData


class TestDeleteUserCommandHandler:
    def test_delete_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        session = Mimic(Spy, Session)
        command = DeleteUserCommand(session, user_id)
        users_repository = Mimic(Spy, PostgresUsersRepository)
        handler = DeleteUserCommandHandler(users_repository)  # type: ignore

        handler.execute(command)

        expect(users_repository.delete).to(have_been_called_with(session, user_id))
        expect(session.commit).to(have_been_called)
        expect(session.close).to(have_been_called)
        expect(session.rollback).not_to(have_been_called)

    def test_raise_error_when_deleting_a_non_existing_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        error_message = f"User with ID: '{user_id}' not found."
        session = Mimic(Spy, Session)
        command = DeleteUserCommand(session, user_id)
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.delete(ANY_ARG).raises(NotFoundUsersRepositoryException(user_id))
        handler = DeleteUserCommandHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(command)).to(raise_error(NotFoundUserException, error_message))
        expect(session.rollback).to(have_been_called)
        expect(session.close).to(have_been_called)
        expect(session.commit).not_to(have_been_called)
