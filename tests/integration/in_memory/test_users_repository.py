from expects import be_empty, equal, expect, raise_error

from src.domain.exceptions import NotFoundUserRepositoryException
from src.domain.user import User
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from tests.test_data import TestData


class TestInMemoryUsersRepositoryIntegration:
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

    def test_save_and_find_all_users_and_delete(self) -> None:
        user = TestData.a_user()
        repository = InMemoryUsersRepository()

        repository.save(user)
        users = repository.find_all()

        expect(users).to(equal([user]))

        repository.delete(user.id)
        users = repository.find_all()

        expect(users).to(be_empty)

    def test_raise_error_when_finding_a_non_existent_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        error_message = f"User with ID: '{user_id.hex}' not found."
        users_repository = InMemoryUsersRepository()

        expect(lambda: users_repository.find_by_id(user_id)).to(
            raise_error(NotFoundUserRepositoryException, error_message)
        )

    def test_raise_error_when_updating_a_non_existent_user(self) -> None:
        user = TestData.a_user()
        error_message = f"User with ID: '{user.id.hex}' not found."
        users_repository = InMemoryUsersRepository()

        expect(lambda: users_repository.update(user)).to(raise_error(NotFoundUserRepositoryException, error_message))

    def test_raise_error_when_deleting_a_non_existent_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        error_message = f"User with ID: '{user_id.hex}' not found."
        users_repository = InMemoryUsersRepository()

        expect(lambda: users_repository.delete(user_id)).to(raise_error(NotFoundUserRepositoryException, error_message))
