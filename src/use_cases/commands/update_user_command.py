from dataclasses import dataclass

from src.domain.user import User


@dataclass
class UpdateUserCommand:
    user: User


class UpdateUserCommandResponse:
    def __init__(self, user: User) -> None:
        self.user = user

    def data(self) -> User:
        return self.user


class UpdateUserCommandHandler:
    def execute(self, command: UpdateUserCommand) -> UpdateUserCommandResponse:
        return UpdateUserCommandResponse(command.user)
