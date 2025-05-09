from dataclasses import dataclass

from src.domain.user import User


@dataclass
class FindAllUsersQueryResponse:
    users: list[User]

    def data(self) -> list[User]:
        return self.users


class FindAllUsersQueryHandler:
    def execute(self) -> FindAllUsersQueryResponse:
        return FindAllUsersQueryResponse(users=[])
