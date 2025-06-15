from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.domain.exceptions import FindAllUsersQueryHandlerException, UsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class FindAllUsersQuery:
    session: Session


@dataclass
class FindAllUsersQueryResponse:
    users: list[User]

    def data(self) -> list[User]:
        return self.users


class FindAllUsersQueryHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, query: FindAllUsersQuery) -> FindAllUsersQueryResponse:
        try:
            session = query.session
            users = self.users_repository.find_all(session)
            session.close()
            return FindAllUsersQueryResponse(users=users)
        except UsersRepositoryException as ex:
            session.close()
            raise FindAllUsersQueryHandlerException(f"{ex}") from ex
