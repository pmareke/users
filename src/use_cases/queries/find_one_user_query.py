from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class FindOneUserQuery:
    session: Session
    user_id: str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FindOneUserQuery):
            return False
        return self.session == other.session and self.user_id == other.user_id


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
            session = query.session
            user = self.users_repository.find_by_id(session, query.user_id)
            session.close()
            return FindOneUserQueryResponse(user=user)
        except NotFoundUsersRepositoryException as ex:
            session.close()
            raise NotFoundUserException(query.user_id) from ex
