from fastapi import Depends, APIRouter, status
from fastapi.responses import JSONResponse

from ..models.DiseaseHistory import PostDiseaseHistory, GetDiseaseHistory
from ..models.Message import Message

from ..services import DiseaseHistoryServices

from typing import List


router = APIRouter(prefix="/disease_history", tags=["disease_history"])


@router.post("/", responses={
    status.HTTP_201_CREATED: {"model": Message}
})
async def create_history(data_hist: PostDiseaseHistory,
                         service: DiseaseHistoryServices = Depends()):
    await service.add_history(data_hist)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "сохранено"}
    )


@router.get("/{uuid_user}", response_model=List[GetDiseaseHistory])
async def get_list_disease_history_user_uuid(uuid_user: str,
                                             service: DiseaseHistoryServices = Depends()):
    list_hist = await service.get_list_hist_by_uuid_user(uuid_user)
    return list_hist
