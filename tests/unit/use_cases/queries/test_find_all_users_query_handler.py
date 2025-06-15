from doublex import ANY_ARG, Mimic, Spy, Stub
from doublex_expects import have_been_called
from expects import equal, expect, raise_error
from sqlalchemy.orm import Session

from src.domain.exceptions import FindAllUsersQueryHandlerException, UsersRepositoryException
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from src.use_cases.queries.find_all_users_query import FindAllUsersQuery, FindAllUsersQueryHandler
from tests.test_data import TestData


class TestFindAllUsersQueryHandler:
    def test_find_all_users(self) -> None:
        user = TestData.a_user()
        session = Mimic(Spy, Session)
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.find_all(session).returns([user])
        query = FindAllUsersQuery(session)
        handler = FindAllUsersQueryHandler(users_repository)  # type: ignore

        response = handler.execute(query)
        users = response.data()

        expect(users).to(equal([user]))
        expect(session.close).to(have_been_called)

    def test_raise_error_when_finding_all_users(self) -> None:
        error_message = "Error finding all users"
        session = Mimic(Spy, Session)
        query = FindAllUsersQuery(session)
        with Mimic(Stub, PostgresUsersRepository) as users_repository:
            users_repository.find_all(ANY_ARG).raises(UsersRepositoryException(error_message))
        handler = FindAllUsersQueryHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(query)).to(raise_error(FindAllUsersQueryHandlerException, error_message))
        expect(session.close).to(have_been_called)
