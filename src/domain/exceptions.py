class NotFoundUserException(Exception):
    def __init__(self, user_id: str) -> None:
        error_message = f"User with ID: '{user_id}' not found."
        super().__init__(error_message)


class NotFoundUsersRepositoryException(Exception):
    def __init__(self, user_id: str) -> None:
        error_message = f"User with ID: '{user_id}' not found."
        super().__init__(error_message)


class UsersRepositoryException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CreateUserCommandHandlerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class FindAllUsersQueryHandlerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
