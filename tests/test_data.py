from uuid import uuid4

from src.domain.user import User


class TestData:
    ANY_USER_ID = uuid4()
    ANY_USER_NAME = "Peter"
    ANY_USER_AGE = 42

    @staticmethod
    def a_user() -> User:
        return User(
            TestData.ANY_USER_ID,
            TestData.ANY_USER_NAME,
            TestData.ANY_USER_AGE,
        )

    @staticmethod
    def a_payload_from_user(user: User) -> dict:
        return {"id": str(user.id), "name": user.name, "age": user.age}
