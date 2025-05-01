from dataclasses import dataclass

from src.domain.user import User


@dataclass
class CreateUserCommand:
    user: User


class CreateUserCommandHandler:
    def execute(self, command: CreateUserCommand) -> None:
        pass
