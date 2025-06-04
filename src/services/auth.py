from datetime import datetime, UTC
import re

from fastapi import Depends, Request, HTTPException, status
from jose import JWTError, jwt

from schemas.auth import UserAuth
from schemas.company import CompanyCreate, CompanyCreateDB
from schemas.session import SessionBase, SessionCreateDB
from schemas.user import UserCreate, UserCreateDB
from constants.user import UserRole
from configs.config import app_settings
from configs.logger import logger
from crud.user import crud_user
from crud.company import crud_company
from crud.session import crud_session
from databases.database import master_session
from security.tools import get_password_hash, verify_password

from models import (
    User,
    Company,
    Session,
)
from utilities.exceptions import ObjectAlreadyExistsError


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"


async def register_company(data: CompanyCreate) -> Company:
    async with master_session() as db, db.begin():
        if await crud_company.get_by_registration_data(
            db=db, inn=data.inn, ogrn=data.ogrn
        ):
            msg = "Компания с указанными данными (ИНН, ОГРН) уже существует"
            raise ObjectAlreadyExistsError(msg)
        return await crud_company.create(
            db=db,
            create_schema=CompanyCreateDB(
                **data.model_dump(exclude_unset=True),
            ),
            commit=False,
        )


async def register_user(data: UserCreate, company_id: int) -> User:
    async with master_session() as db, db.begin():
        if await crud_user.get_by_login_or_email(
            db=db, login=data.login, email=data.email
        ):
            msg = (
                "Пользователь с указанными данными"
                " (логин, адрес почты) уже существует"
            )
            raise ObjectAlreadyExistsError(msg)
        hashed_password = get_password_hash(data.password)
        # TODO(tyyrok@gmail.com): implement phone number verification
        return await crud_user.create(
            db=db,
            create_schema=UserCreateDB(
                **data.model_dump(exclude_unset=True),
                company_id=company_id,
                hashed_password=hashed_password,
                role=UserRole.admin,
            ),
            commit=False,
        )


async def authenticate_user(data: UserAuth) -> None | User:
    async with master_session() as db, db.begin():
        user = None
        if re.match(EMAIL_REGEX, data.login_or_email):
            user = await crud_user.get_by_email(
                db=db, email=data.login_or_email
            )
        else:
            user = await crud_user.get_by_login(
                db=db, login=data.login_or_email
            )
        if not user or not verify_password(
            data.password, user.hashed_password
        ):
            return None
        return user


async def create_new_session(
    data: SessionBase, token: str, user_id: int
) -> Session:
    async with master_session() as db, db.begin():
        if existing_session := await crud_session.get_by_device(
            db=db,
            device=data.device,
            user_id=user_id,
        ):
            logger.info("Нашлась сессия с аналогичного типа устройства")
            await crud_session.remove(
                db=db,
                obj_id=existing_session.id,
                commit=False,
            )
        return await crud_session.create(
            db=db,
            create_schema=SessionCreateDB(
                **data.model_dump(exclude_unset=True),
                jwt_token=token,
                user_id=user_id,
            ),
            commit=False,
        )


async def delete_session(token: str) -> None:
    async with master_session() as db, db.begin():
        if existing_session := await crud_session.get_by_jwt(
            db=db, token=token
        ):
            await crud_session.remove(
                db=db,
                obj_id=existing_session.id,
            )


async def get_user(user_id: int) -> User:
    async with master_session() as db:
        if user := await crud_user.get_by_id(db=db, obj_id=user_id):
            if not user.is_active:
                await crud_user.update_by_id(
                    db=db,
                    db_obj_id=user.id,
                    update_data={"is_active": True},
                    commit=False,
                )
            return user


async def get_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token, app_settings.SECRET_KEY, app_settings.ALGORITHM
        )
    except JWTError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from ex
    expire = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(UTC).timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        return int(user_id)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from ex


async def get_token(request: Request) -> str:
    if request.headers.get("Authorization"):
        token = str(request.headers.get("Authorization")).split(" ")[1]
    else:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    user_id = await get_user_id_from_token(token)
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
