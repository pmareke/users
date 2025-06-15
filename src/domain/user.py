from uuid import UUID

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Numeric, nullable=False)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id and self.name == other.name and self.age == other.age

    def json(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "age": self.age,
        }
