from doublex import ANY_ARG, Mimic, Stub
from expects import expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import UsersRepositoryException
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from tests.test_data import TestData


class TestPostgresUsersRepositoryIntegration:
    def test_raise_error_when_finding_all_users(self) -> None:
        error = "any-error"
        error_message = f"An error occurred while trying to find all users, ex: '{error}'."
        with Mimic(Stub, Session) as session:
            session.scalars(ANY_ARG).raises(Exception(error))
        users_repository = PostgresUsersRepository()

        expect(lambda: users_repository.find_all(session)).to(raise_error(UsersRepositoryException, error_message))

    def test_raise_error_when_updating_a_non_existent_user(self) -> None:
        user = TestData.a_user()
        error = "any-error"
        error_message = f"An error occurred while trying to save a user, ex: '{error}'."
        with Mimic(Stub, Session) as session:
            session.add(ANY_ARG).raises(Exception(error))
        users_repository = PostgresUsersRepository()

        expect(lambda: users_repository.save(session, user)).to(raise_error(UsersRepositoryException, error_message))
