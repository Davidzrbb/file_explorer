from functools import lru_cache
from os import getenv

from pydantic import BaseSettings

ENV = getenv("ENV", "dev")


class Settings(BaseSettings):
    app_name: str = 'file_explorer'
    app_version: str = '0.0.1'
    app_env: str = ENV


@lru_cache
def get_settings():
    return Settings(
        _env_file=f'.env.{ENV}',
    )
