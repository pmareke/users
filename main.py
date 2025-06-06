from fastapi import FastAPI

from src.delivery.api.v1.users.users_router import users_router

app = FastAPI(
    title="CRUD Users API",
    description="A simple API for managing users with CRUD operations.",
)

app.include_router(
    prefix="/api/v1/users",
    router=users_router,
    tags=["users"],
)
