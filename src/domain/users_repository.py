from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.user import User


class UsersRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError
