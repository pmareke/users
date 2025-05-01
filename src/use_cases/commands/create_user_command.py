from dataclasses import dataclass

from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class CreateUserCommand:
    user: User


class CreateUserCommandHandler:
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    def execute(self, command: CreateUserCommand) -> None:
        self.users_repository.save(command.user)
