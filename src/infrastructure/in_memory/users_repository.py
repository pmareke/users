from src.domain.exceptions import NotFoundUsersRepositoryException, UsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


class InMemoryUsersRepository(UsersRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(self, user: User) -> None:
        try:
            self._users[user.id] = user
        except Exception as ex:
            raise UsersRepositoryException(f"{ex}") from ex

    def find_all(self) -> list[User]:
        try:
            return list(self._users.values())
        except Exception as ex:
            raise UsersRepositoryException(f"{ex}") from ex

    def find_by_id(self, user_id: str) -> User:
        try:
            return self._users[user_id]
        except KeyError as ex:
            raise NotFoundUsersRepositoryException(user_id) from ex

    def update(self, user: User) -> User:
        if not self._users.get(user.id):
            raise NotFoundUsersRepositoryException(user.id)

        self._users[user.id] = user
        return user

    def delete(self, user_id: str) -> None:
        try:
            del self._users[user_id]
        except KeyError as ex:
            raise NotFoundUsersRepositoryException(user_id) from ex
