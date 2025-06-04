from datetime import datetime, timedelta, UTC

from jose import JWTError, jwt
from configs.config import app_settings
from utilities.exceptions import TokenExpiredException


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=90)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM
    )


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token, app_settings.SECRET_KEY, algorithm=app_settings.ALGORITHM
        )
    except JWTError as ex:
        raise TokenExpiredException from ex
