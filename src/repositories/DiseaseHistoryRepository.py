from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy import text
from ..tables import DiseaseHistory
from ..database import get_session

from fastapi import Depends

from typing import List


class DiseaseHistoryRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.__session: AsyncSession = session

    async def count_row(self) -> int:
        response = select(func.count(DiseaseHistory.id))
        result = await self.__session.execute(response)
        return result.scalars().first()

    async def get(self, id_dis: int) -> DiseaseHistory:
        result = await self.__session.get(DiseaseHistory, id_dis)
        return result

    async def get_list_disease_history_by_id_user(self, start: int, limit: int, id_user: int) -> List[DiseaseHistory]:
        response = select(DiseaseHistory).where(DiseaseHistory.id_user == id_user).offset(start).fetch(limit).order_by(DiseaseHistory.id)
        result = await self.__session.execute(response)
        return result.unique().scalars().all()

    async def add(self, hist: DiseaseHistory):
        try:
            self.__session.add(hist)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def update(self, hist: DiseaseHistory):
        try:
            self.__session.add(hist)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def delete(self, hist):
        try:
            await self.__session.delete(hist)
            await self.__session.commit()
        except:
            await self.__session.rollback()
            raise Exception

    async def get_by_uuid(self, uuid: str) -> DiseaseHistory:
        query = select(DiseaseHistory).where(DiseaseHistory.uuid == uuid)
        response = await self.__session.execute(query)
        return response.scalars().first()
