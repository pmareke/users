from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.domain.exceptions import CreateUserCommandHandlerException, UsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class CreateUserCommand:
    session: Session
    user: User

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CreateUserCommand):
            return False
        return self.session == other.session and self.user == other.user


class CreateUserCommandHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, command: CreateUserCommand) -> None:
        try:
            session = command.session
            self.users_repository.save(session, command.user)
            session.commit()
            session.close()
        except UsersRepositoryException as ex:
            session.rollback()
            session.close()
            raise CreateUserCommandHandlerException(f"{ex}") from ex
