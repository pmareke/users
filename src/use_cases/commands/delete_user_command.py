from dataclasses import dataclass
from uuid import UUID

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.domain.users_repository import UsersRepository


@dataclass
class DeleteUserCommand:
    user_id: UUID


class DeleteUserCommandHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, command: DeleteUserCommand) -> None:
        try:
            self.users_repository.delete(command.user_id)
        except NotFoundUsersRepositoryException as ex:
            raise NotFoundUserException(command.user_id) from ex
