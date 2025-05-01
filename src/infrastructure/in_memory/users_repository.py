from src.domain.user import User
from src.domain.users_repository import UsersRepository


class InMemoryUsersRepository(UsersRepository):
    def save(self, user: User) -> None:
        pass
