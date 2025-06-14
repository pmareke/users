from abc import ABC, abstractmethod

from src.domain.user import User


class UsersRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str) -> None:
        raise NotImplementedError
