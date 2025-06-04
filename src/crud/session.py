from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models import Session
from schemas.session import SessionCreateDB, SessionUpdateDB


class CRUDSession(BaseAsyncCRUD[Session, SessionCreateDB, SessionUpdateDB]):
    async def get_by_device(
        self, db: AsyncSession, device: str, user_id: int
    ) -> Optional[Session]:
        stmt = select(self.model).where(
            self.model.device == device,
            self.model.user_id == user_id,
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_jwt(
        self, db: AsyncSession, token: str
    ) -> Optional[Session]:
        stmt = select(self.model).where(
            self.model.jwt_token == token,
        )
        result = await db.execute(stmt)
        return result.scalars().first()


crud_session = CRUDSession(Session)
