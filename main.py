import contextlib
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from alembic import command
from alembic.config import Config
from src.delivery.api.v1.users.users_router import users_router


def run_sql_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    run_sql_migrations()

    yield


app = FastAPI(
    title="CRUD Users API",
    description="A simple API for managing users with CRUD operations.",
    lifespan=lifespan,
)

app.include_router(
    prefix="/api/v1/users",
    router=users_router,
    tags=["users"],
)
