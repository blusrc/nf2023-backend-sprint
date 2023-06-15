from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .adapters.s3_service import S3Service
from .repository.repository import ShanyrakRepository


class ShanyrakConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800


config = ShanyrakConfig()


class Service:
    def __init__(
        self,
        repository: ShanyrakRepository,
        jwt_svc: JwtService,
        s3_svc: S3Service
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.s3_service = s3_svc


def get_service():
    repository = ShanyrakRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    s3_svc = S3Service()

    svc = Service(repository, jwt_svc, s3_svc)
    return svc
