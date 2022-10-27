from fastapi import APIRouter

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

from.app import add_app_routes

add_app_routes(router)
