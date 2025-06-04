from pathlib import Path

from .base import BaseSetting

BASE_DIR = Path(__file__).parent.parent


class AppSettings(BaseSetting):
    BASE_DIR: Path = BASE_DIR
    SERVICE_NAME: str
    SERVICE_VERSION: str
    API_VERSION: str
    ENVIRONMENT: str
    SERVICE_PORT: int = 8080
    SECRET_KEY: str
    ALGORITHM: str
    LOGIN_URL: str


class DBSettings(BaseSetting):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POOL_SIZE: int = 40
    POOL_MAX_OVERFLOW: int = 10
    SQL_ECHO: bool = True

    @property
    def db_uri(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class RedisSetting(BaseSetting):
    REDIS_HOST: str
    REDIS_PORT: int


class S3StorageSettings(BaseSetting):
    AWS_ACCESS_KEY_ID: str
    AWS_S3_ENDPOINT_URL: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_DEFAULT_ACL: str = "public-read"
    AWS_S3_USE_SSL: bool = True
    AWS_QUERYSTRING_AUTH: bool = False
    AWS_S3_PRODUCT_FOLDER_NAME: str


class MailSettings(BaseSetting):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True


app_settings = AppSettings()
db_settings = DBSettings()
redis_settings = RedisSetting()
mail_settings = MailSettings()
storage_settings = S3StorageSettings()
