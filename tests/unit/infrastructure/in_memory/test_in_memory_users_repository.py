from expects import equal, expect

from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from tests.test_data import TestData


class TestInMemoryUsersRepository:
    def test_save__and_find_all_users(self) -> None:
        user = TestData.a_user()
        repository = InMemoryUsersRepository()

        repository.save(user)
        users = repository.find_all()

        expect(users).to(equal([user]))

    def test_save__and_find_one_user(self) -> None:
        user = TestData.a_user()
        repository = InMemoryUsersRepository()

        repository.save(user)
        found_user = repository.find_by_id(user.id)

        expect(found_user).to(equal(user))
