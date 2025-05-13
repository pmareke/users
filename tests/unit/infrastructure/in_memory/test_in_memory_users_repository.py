from expects import equal, expect

from src.domain.user import User
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from tests.test_data import TestData


class TestInMemoryUsersRepository:
    def test_save_and_find_all_users(self) -> None:
        user = TestData.a_user()
        repository = InMemoryUsersRepository()

        repository.save(user)
        users = repository.find_all()

        expect(users).to(equal([user]))

    def test_save_and_find_one_user(self) -> None:
        user = TestData.a_user()
        repository = InMemoryUsersRepository()

        repository.save(user)
        found_user = repository.find_by_id(user.id)

        expect(found_user).to(equal(user))

    def test_update_one_user(self) -> None:
        user = TestData.a_user()
        new_user = User(user.id, user.name, user.age + 1)
        repository = InMemoryUsersRepository()

        repository.save(user)
        updated_user = repository.update(new_user)
        users = repository.find_all()

        expect(users).to(equal([updated_user]))
