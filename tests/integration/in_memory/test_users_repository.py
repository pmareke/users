from expects import expect, raise_error

from src.domain.exceptions import NotFoundUserRepositoryException
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository
from tests.test_data import TestData


class TestInMemoryUsersRepositoryIntegration:
    def test_raise_error_when_deleting_a_non_existent_user(self) -> None:
        user_id = TestData.ANY_USER_ID
        error_message = f"User with ID: '{user_id.hex}' not found."
        users_repository = InMemoryUsersRepository()

        expect(lambda: users_repository.delete(user_id)).to(raise_error(NotFoundUserRepositoryException, error_message))
