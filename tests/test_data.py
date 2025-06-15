from uuid import uuid4

from src.domain.user import User


class TestData:
    ANY_USER_ID = uuid4()
    ANY_USER_NAME = "Peter"
    ANY_USER_AGE = 42

    @staticmethod
    def a_user() -> User:
        return User(id=TestData.ANY_USER_ID, name=TestData.ANY_USER_NAME, age=TestData.ANY_USER_AGE)

    @staticmethod
    def a_payload_from_a_user(user: User) -> dict:
        return {"id": str(user.id), "name": user.name, "age": user.age}
