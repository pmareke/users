from doublex import Mimic, Stub
from expects import equal, expect

from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from src.use_cases.queries.find_all_users_query import FindAllUsersQueryHandler
from tests.test_data import TestData


class TestFindAllUsersQueryHandler:
    def test_find_all_users(self) -> None:
        user = TestData.a_user()
        with Mimic(Stub, InMemoryUsersRepository) as users_repository:
            users_repository.find_all().returns([user])
        handler = FindAllUsersQueryHandler(users_repository)  # type: ignore

        response = handler.execute()
        users = response.data()

        expect(users).to(equal([user]))
