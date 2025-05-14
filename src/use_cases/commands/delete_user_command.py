from dataclasses import dataclass
from uuid import UUID

from src.domain.users_repository import UsersRepository


@dataclass
class DeleteUserCommand:
    user_id: UUID


class DeleteUserCommandHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, command: DeleteUserCommand) -> None:
        self.users_repository.delete(command.user_id)
