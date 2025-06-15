from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.domain.exceptions import NotFoundUsersRepositoryException, UsersRepositoryException
from src.domain.user import User
from src.domain.users_repository import UsersRepository


class PostgresUsersRepository(UsersRepository):
    def save(self, session: Session, user: User) -> None:
        try:
            session.add(user)
        except Exception as ex:
            raise UsersRepositoryException(f"An error occurred while trying to save a user, ex: '{ex}'.") from ex

    def find_all(self, session: Session) -> list[User]:
        try:
            statement = select(User)
            return list(session.scalars(statement).all())
        except Exception as ex:
            raise UsersRepositoryException(f"An error occurred while trying to find all users, ex: '{ex}'.") from ex

    def find_by_id(self, session: Session, user_id: str) -> User:
        try:
            statement = select(User).where(User.id == user_id)
            return session.execute(statement).scalar_one()
        except NoResultFound as ex:
            raise NotFoundUsersRepositoryException(user_id) from ex

    def update(self, session: Session, user: User) -> User:
        existing_user = self.find_by_id(session, user.id)
        existing_user.name = user.name
        existing_user.age = user.age
        return existing_user

    def delete(self, session: Session, user_id: str) -> None:
        user = self.find_by_id(session, user_id)
        session.delete(user)
