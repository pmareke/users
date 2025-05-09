from dataclasses import dataclass

from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class FindAllUsersQueryResponse:
    users: list[User]

    def data(self) -> list[User]:
        return self.users


class FindAllUsersQueryHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self) -> FindAllUsersQueryResponse:
        users = self.users_repository.find_all()
        return FindAllUsersQueryResponse(users=users)
