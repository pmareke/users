from doublex import ANY_ARG, Mimic, Stub
from expects import equal, expect, raise_error

from src.domain.exceptions import NotFoundUserException, NotFoundUserRepositoryException
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.queries.find_one_user_query import (
    FindOneUserQuery,
    FindOneUserQueryHandler,
)
from tests.test_data import TestData


class TestFindOneUserQueryHandler:
    def test_find_one_user(self) -> None:
        user = TestData.a_user()
        query = FindOneUserQuery(user.id)
        with Mimic(Stub, InMemoryUsersRepository) as users_repository:
            users_repository.find_by_id(user.id).returns(user)
        handler = FindOneUserQueryHandler(users_repository)  # type: ignore

        response = handler.execute(query)
        found_user = response.data()

        expect(found_user).to(equal(user))

    def test_raise_error_when_finding_a_non_existing_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        query = FindOneUserQuery(user_id)
        error_message = f"User with ID: '{user_id.hex}' not found."
        with Mimic(Stub, InMemoryUsersRepository) as users_repository:
            users_repository.find_by_id(ANY_ARG).raises(NotFoundUserRepositoryException(user_id))
        handler = FindOneUserQueryHandler(users_repository)  # type: ignore

        expect(lambda: handler.execute(query)).to(raise_error(NotFoundUserException, error_message))
