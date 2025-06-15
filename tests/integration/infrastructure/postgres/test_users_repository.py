import pytest
from expects import be_empty, equal, expect, raise_error
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.common.settings import settings
from src.domain.exceptions import NotFoundUsersRepositoryException
from src.domain.user import User
from src.infrastructure.postgres.users_repository import PostgresUsersRepository
from tests.test_data import TestData


class TestPostgresUsersRepositoryIntegration:
    @pytest.fixture(autouse=True)
    def session(self):  # noqa
        engine = create_engine(f"postgresql://{settings.database_dsn}")
        session = Session(engine)

        yield session

        session.execute(text("DELETE FROM users"))

        session.commit()
        session.close()

    def test_save_and_find_all_and_delete_users(self, session: Session) -> None:
        user = TestData.a_user()
        users_repository = PostgresUsersRepository()

        users_repository.save(session, user)
        session.commit()

        users = users_repository.find_all(session)

        expect(users).to(equal([user]))

        users_repository.delete(session, user.id)
        session.commit()

        users = users_repository.find_all(session)

        expect(users).to(be_empty)

    def test_save_and_find_one_user(self, session: Session) -> None:
        user = TestData.a_user()
        users_repository = PostgresUsersRepository()

        users_repository.save(session, user)
        session.commit()

        existing_user = users_repository.find_by_id(session, user.id)

        expect(existing_user).to(equal(user))

    def test_update_one_user(self, session: Session) -> None:
        user = TestData.a_user()
        edited_user = User(id=user.id, name="new_name", age=user.age)

        users_repository = PostgresUsersRepository()

        users_repository.save(session, user)
        session.commit()

        users_repository.update(session, edited_user)
        session.commit()

        existing_user = users_repository.find_by_id(session, user.id)

        expect(existing_user).to(equal(edited_user))

    def test_raise_error_when_finding_a_non_existent_user(self, session: Session) -> None:
        user_id = "non_existent_id"
        error_message = f"User with ID: '{user_id}' not found."
        users_repository = PostgresUsersRepository()

        expect(lambda: users_repository.find_by_id(session, user_id)).to(
            raise_error(NotFoundUsersRepositoryException, error_message)
        )

    def test_raise_error_when_updating_a_non_existent_user(self, session: Session) -> None:
        user = TestData.a_user()
        error_message = f"User with ID: '{user.id}' not found."
        users_repository = PostgresUsersRepository()

        expect(lambda: users_repository.update(session, user)).to(
            raise_error(NotFoundUsersRepositoryException, error_message)
        )

    def test_raise_error_when_deleting_a_non_existent_user(self, session: Session) -> None:
        user_id = "non_existent_id"
        error_message = f"User with ID: '{user_id}' not found."
        users_repository = PostgresUsersRepository()

        expect(lambda: users_repository.delete(session, user_id)).to(
            raise_error(NotFoundUsersRepositoryException, error_message)
        )
