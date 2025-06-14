from dataclasses import dataclass

from src.domain.exceptions import NotFoundUserException, NotFoundUsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


@dataclass
class UpdateUserCommand:
    user: User


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
            user = self.users_repository.update(command.user)
            return UpdateUserCommandResponse(user)
        except NotFoundUsersRepositoryException as ex:
            raise NotFoundUserException(command.user.id) from ex
