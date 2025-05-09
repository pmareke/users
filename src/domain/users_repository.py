from abc import ABC, abstractmethod

from src.domain.user import User


class UsersRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[User]:
        raise NotImplementedError
