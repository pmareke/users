from uuid import UUID


class NotFoundUserException(Exception):
    def __init__(self, user_id: UUID) -> None:
        error_message = f"User with ID: '{user_id.hex}' not found."
        super().__init__(error_message)


class NotFoundUserRepositoryException(Exception):
    def __init__(self, user_id: UUID) -> None:
        error_message = f"User with ID: '{user_id.hex}' not found."
        super().__init__(error_message)


class CreateUserCommandHandlerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class FindAllUsersQueryHandlerException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
