from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models import User
from schemas.user import UserUpdateDB, UserCreateDB


class CRUDUser(BaseAsyncCRUD[User, UserCreateDB, UserUpdateDB]):
    async def get_by_login_or_email(
        self, db: AsyncSession, login: str, email: Optional[str] = None
    ) -> Optional[User]:
        if email:
            stmt = select(self.model).where(
                or_(self.model.login == login, self.model.email == email)
            )
        else:
            stmt = select(self.model).where(self.model.login == login)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_login(
        self, db: AsyncSession, login: str
    ) -> Optional[User]:
        stmt = select(self.model).where(self.model.login == login)
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_email(
        self, db: AsyncSession, email: str
    ) -> Optional[User]:
        stmt = select(self.model).where(self.model.email == email)
        result = await db.execute(stmt)
        return result.scalars().first()


crud_user = CRUDUser(User)
