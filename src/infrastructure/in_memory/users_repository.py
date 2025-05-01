from src.domain.user import User
from src.domain.users_repository import UsersRepository


class InMemoryUsersRepository(UsersRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        self._users[user.name] = user

    def find_all(self) -> list[User]:
        return list(self._users.values())
