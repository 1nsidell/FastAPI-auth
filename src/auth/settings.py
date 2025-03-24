import os
from pathlib import Path
from typing import Dict

from pydantic import BaseModel, HttpUrl
from sqlalchemy import URL


# ----------------------------- BaseProjectConfig -----------------------------
class Paths:
    ROOT_DIR_SRC: Path = Path(__file__).parent.parent
    PATH_TO_BASE_FOLDER = Path(__file__).parent.parent.parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8001


class ApiPrefix(BaseModel):
    prefix: str = "/api/auth"
    healthcheck: str = "/healthcheck"
    liveness: str = "/liveness"
    readiness: str = "/readiness"
    v1_prefix: str = "/v1"
    signin: str = "/signin"
    signup: str = "/signup"


class AuthJWTConfig(BaseModel):
    PRIVATE_KEY_PATH: Path = (
        Path(__file__).parent / "certs" / "jwt" / "private.pem"
    )
    PUBLIC_KEY_PATH: Path = (
        Path(__file__).parent / "certs" / "jwt" / "public.pem"
    )
    DECODE_ALGORITHMS: str = os.getenv(
        "DECODE_ALGORITHMS", "RS256,HS256"
    ).split(",")
    ENCODE_ALGORITHM: str = os.getenv("ENCODE_ALGORITHM", "RS256")
    ACCESS_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_EXPIRE_MINUTES", "15"))
    REFRESH_EXPIRE_DAYS: int = int(os.getenv("REFRESH_EXPIRE_DAYS", "30"))
    CONFIRMATION_TIME: int = int(os.getenv("CONFIRMATION_TIME_DAYS", "1"))


class DatabaseConfig(BaseModel):
    """Config to connect to SQL database"""

    DRIVER: str = os.getenv("DB_DRIVER", "postgresql+asyncpg")
    USER: str = os.getenv("DB_USER", "guest")
    PASS: str = os.getenv("DB_PASS", "guest")
    HOST: str = os.getenv("DB_HOST", "localhost")
    PORT: int = int(os.getenv("DB_PORT", "5432"))
    NAME: str = os.getenv("DB_NAME", "postgres")
    ECHO: bool = bool(int(os.getenv("DB_ECHO", "0")))
    ECHO_POOL: bool = bool(int(os.getenv("DB_ECHO_POOL", "0")))
    POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.DRIVER,
            username=self.USER,
            password=self.PASS,
            host=self.HOST,
            port=self.PORT,
            database=self.NAME,
        )

    naming_convention: Dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig(BaseModel):
    """Config to connect to Redis database"""

    HOST: str = os.getenv("REDIS_HOST", "loaclhost")
    PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    CACHE_DB: int = int(os.getenv("REDIS_CACHE_DB", "0"))
    USERNAME: str = os.getenv("REDIS_USERNAME", "guest")
    PASSWORD: str = os.getenv("REDIS_PASSWORD", "guest")

    CACHE_LIFETIME: int = int(os.getenv("REDIS_CACHE_LIFETIME", "5"))

    @property
    def auth_cache_url(self) -> str:
        return f"redis://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.CACHE_DB}"


class RabbitMQConfig(BaseModel):
    USERNAME: str = os.getenv("RABBIT_USERNAME", "guest")
    PASSWORD: str = os.getenv("RABBIT_PASSWORD", "guest")
    HOST: str = os.getenv("RABBIT_HOST", "localhost")
    PORT: int = int(os.getenv("RABBIT_PORT", "5672"))
    VHOST: str = os.getenv("RABBIT_VHOST", "")
    TIMEOUT: int = int(os.getenv("RABBIT_TIMEOUT", 30))

    RABBIT_EMAIL_QUEUE: str = os.getenv("RABBIT_EMAIL_QUEUE")

    @property
    def url(self) -> str:
        return f"amqp://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.VHOST}"


class Gateways(BaseModel):
    USERS_MANAGEMENT: HttpUrl = os.getenv("USERS_MANAGEMENT")

    REQUEST_TIMEOUT: int = float(os.getenv("REQUEST_TIMEOUT", "1.5"))


class Settings:
    mode: str = os.getenv("MODE", "PROD")
    api_key: str = os.getenv("API_KEY", "secret")
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig = DatabaseConfig()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    redis: RedisConfig = RedisConfig()
    paths: Paths = Paths()
    gateways: Gateways = Gateways()
    rmq: RabbitMQConfig = RabbitMQConfig()


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
