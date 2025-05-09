from dataclasses import dataclass
from uuid import UUID

from src.domain.user import User
from tests.test_data import TestData


@dataclass
class FindOneUserQuery:
    user_id: UUID


@dataclass
class FindOneUserQueryResponse:
    user: User

    def data(self) -> User:
        return self.user


class FindOneUserQueryHandler:
    def execute(self, query: FindOneUserQuery) -> FindOneUserQueryResponse:
        user = TestData.a_user()
        return FindOneUserQueryResponse(user=user)
