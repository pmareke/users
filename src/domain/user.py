from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    id: UUID
    name: str
    age: int

    def json(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "age": self.age,
        }
