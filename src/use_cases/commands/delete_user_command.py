from dataclasses import dataclass

from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.domain.users_repository import UsersRepository


@dataclass
class DeleteUserCommand:
    session: Session
    user_id: str


class DeleteUserCommandHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, command: DeleteUserCommand) -> None:
        try:
            session = command.session
            self.users_repository.delete(session, command.user_id)
            session.commit()
            session.close()
        except NotFoundUsersRepositoryException as ex:
            session.rollback()
            session.close()
            raise NotFoundUserException(command.user_id) from ex
