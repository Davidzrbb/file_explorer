import routers as routers
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from config import get_settings


def create_app():
    settings = get_settings()

    app = FastAPI(
        name=settings.app_name,
        title=settings.app_name,
        version=settings.app_version,
        description='Api de MyFlows permettant de gérer les fichiers en retournant des informations '
                    'sur les fichiers et les dossiers des flux SEA',
        servers=[]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(
        routers.api.router,
    )

    return app
