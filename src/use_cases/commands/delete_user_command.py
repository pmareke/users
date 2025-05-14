from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteUserCommand:
    user_id: UUID


class DeleteUserCommandHandler:
    def execute(self, command: DeleteUserCommand) -> None:
        pass
