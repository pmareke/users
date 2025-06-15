from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class UpdateUserCommand:
    session: Session
    user: User

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UpdateUserCommand):
            return False
        return self.session == other.session and self.user == other.user


class UpdateUserCommandResponse:
    def __init__(self, user: User) -> None:
        self.user = user

    def data(self) -> User:
        return self.user


class UpdateUserCommandHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, command: UpdateUserCommand) -> UpdateUserCommandResponse:
        try:
            session = command.session
            user = self.users_repository.update(command.session, command.user)
            session.commit()
            session.close()
            return UpdateUserCommandResponse(user)
        except NotFoundUsersRepositoryException as ex:
            session.rollback()
            session.close()
            raise NotFoundUserException(command.user.id) from ex
