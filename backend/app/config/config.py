import os

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()
ENV = os.getenv('ENV') if os.getenv('ENV') else 'local'


class Settings(BaseSettings):
    ENV: str = ENV

    class Config:
        env_file: str = f'{ENV}.env'
        env_file_encoding: str = 'utf-8'
        extra: str = 'forbid'

        load_dotenv(dotenv_path=f'{ENV}.env')


class LoadSetting:
    """ settings load """

    def __call__(self) -> Settings:
        return Settings()
