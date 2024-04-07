from fastapi import APIRouter, Depends, status, Form, File, UploadFile
from fastapi.responses import JSONResponse

from ..services import UserServices
from ..models.Message import Message
from ..models.User import UserPost, UserGet


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", responses={
    status.HTTP_201_CREATED: {"model": Message}
})
async def add_user(
        login: str = Form(...),
        password: str = Form(...),
        id_type: int = Form(...),
        face_img: UploadFile = File(...),
        services: UserServices = Depends()
):
    user_model = UserPost(
        login=login,
        password=password,
        id_type=id_type
    )
    try:
        await services.registrate_user(user_model, face_img)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "сохранено"}
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Лицо не найдено на изображении"}
        )


@router.post("/get_user/face_recognize", response_model=UserGet)
async def get_user_by_face(
        face_img: UploadFile = File(...),
        services: UserServices = Depends()
):
    user_entity = await services.get_user_by_face(face_img)
    return user_entity