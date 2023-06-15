from pydantic import BaseSettings

from app.config import database

from .adapters.jwt_service import JwtService
from .adapters.here_service import HereService
from .adapters.s3_service import S3Service
from .repository.repository import AuthRepository


class AuthConfig(BaseSettings):
    JWT_ALG: str = "HS256"
    JWT_SECRET: str = "YOUR_SUPER_SECRET_STRING"
    JWT_EXP: int = 10_800
    HERE_API_KEY: str


config = AuthConfig()


class Service:
    def __init__(
        self,
        repository: AuthRepository,
        jwt_svc: JwtService,
        s3_svc: S3Service,
        here_svc: HereService
    ):
        self.repository = repository
        self.jwt_svc = jwt_svc
        self.s3_service = S3Service()
        self.here_service = HereService()


def get_service():
    repository = AuthRepository(database)
    jwt_svc = JwtService(config.JWT_ALG, config.JWT_SECRET, config.JWT_EXP)
    s3_service = S3Service()
    here_service = HereService(config.HERE_API_KEY)

    svc = Service(repository, jwt_svc, s3_service, here_service)
    return svc
