from dataclasses import dataclass

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class FindOneUserQuery:
    user_id: str


@dataclass
class FindOneUserQueryResponse:
    user: User

    def data(self) -> User:
        return self.user


class FindOneUserQueryHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, query: FindOneUserQuery) -> FindOneUserQueryResponse:
        try:
            user = self.users_repository.find_by_id(query.user_id)
            return FindOneUserQueryResponse(user=user)
        except NotFoundUsersRepositoryException as ex:
            raise NotFoundUserException(query.user_id) from ex
