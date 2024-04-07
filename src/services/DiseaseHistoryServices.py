from fastapi import Depends
from uuid import uuid4

from ..models.DiseaseHistory import PostDiseaseHistory, GetDiseaseHistory
from ..tables import DiseaseHistory

from ..repositories import DiseaseHistoryRepository, UserRepository

from typing import List

class DiseaseHistoryServices:
    def __init__(self,
                 repo: DiseaseHistoryRepository = Depends(),
                 user_repo: UserRepository = Depends()):
        self.__repo: DiseaseHistoryRepository = repo
        self.__user_repo: UserRepository = user_repo

    async def add_history(self, hist: PostDiseaseHistory):
        user = await self.__user_repo.get_by_uuid(hist.uuid_user)
        entity = DiseaseHistory(
            uuid=uuid4(),
            name=hist.name,
            description=hist.description,
            id_user=user.id
        )
        await self.__repo.add(entity)

    async def get_list_hist_by_uuid_user(self, uuid_user: str) -> List[GetDiseaseHistory]:
        user = await self.__user_repo.get_by_uuid(uuid_user)
        entity = await self.__repo.get_list_disease_history_by_id_user(0, 100, user.id)
        return [GetDiseaseHistory.model_validate(i, from_attributes=True) for i in entity]
