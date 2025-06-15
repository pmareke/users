from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called
from expects import equal, expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from src.use_cases.queries.find_one_user_query import (
    FindOneUserQuery,
    FindOneUserQueryHandler,
)
from tests.test_data import TestData


class TestFindOneUserQueryHandler:
    def test_find_one_user(self) -> None:
        user = TestData.a_user()
        session = Mimic(Spy, Session)
        query = FindOneUserQuery(session, user.id)
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.find_by_id(session, user.id).returns(user)
        handler = FindOneUserQueryHandler(users_repository)  # type: ignore

        response = handler.execute(query)
        found_user = response.data()

        expect(found_user).to(equal(user))
        expect(session.close).to(have_been_called)

    def test_raise_error_when_finding_a_non_existing_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        session = Mimic(Spy, Session)
        query = FindOneUserQuery(session, user_id)
        error_message = f"User with ID: '{user_id}' not found."
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.find_by_id(ANY_ARG).raises(NotFoundUsersRepositoryException(user_id))
        handler = FindOneUserQueryHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(query)).to(raise_error(NotFoundUserException, error_message))
        expect(session.close).to(have_been_called)
