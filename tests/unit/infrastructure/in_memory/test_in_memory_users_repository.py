from uuid import uuid4

from expects import equal, expect

from src.domain.user import User
from src.infrastructure.in_memory.users_repository import InMemoryUsersRepository


class TestInMemoryUsersRepository:
    def test_save_user(self) -> None:
        user_id = uuid4()
        user = User(id=user_id, name="Peter", age=42)
        repository = InMemoryUsersRepository()

        repository.save(user)
        users = repository.find_all()

        expect(users).to(equal([user]))
