from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from crud.async_crud import BaseAsyncCRUD
from models import Company
from schemas.company import CompanyCreateDB, CompanyUpdateDB


class CRUDCompany(BaseAsyncCRUD[Company, CompanyCreateDB, CompanyUpdateDB]):
    async def get_by_registration_data(
        self, db: AsyncSession, inn: str, ogrn: str
    ) -> Optional[Company]:
        stmt = select(self.model).where(
            or_(
                self.model.inn == inn,
                self.model.ogrn == ogrn,
            )
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_inn(
        self, db: AsyncSession, inn: str
    ) -> Optional[Company]:
        stmt = select(self.model).where(
            self.model.inn == inn,
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_ogrn(
        self, db: AsyncSession, ogrn: str
    ) -> Optional[Company]:
        stmt = select(self.model).where(
            self.model.ogrn == ogrn,
        )
        result = await db.execute(stmt)
        return result.scalars().first()


crud_company = CRUDCompany(Company)
