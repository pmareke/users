from doublex import Mimic, Stub
from expects import equal, expect

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
