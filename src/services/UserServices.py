from fastapi import Depends, UploadFile

from ..repositories import UserRepository
from ..models.User import UserPost, UserGet
from ..tables import FaceUser, User

from deepface import DeepFace
import numpy as np
from PIL import Image
from io import BytesIO
from uuid import uuid4


class UserServices:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.__user_repo: UserRepository = user_repo

    def load_image_into_numpy_array(self, data):
        return np.array(Image.open(BytesIO(data)))

    async def embedding_face(self, face_img):
        obj = DeepFace.represent(face_img,
                                 model_name="Facenet",
                                 detector_backend="mtcnn"
                                 )
        embedding = obj[0]["embedding"]
        return embedding

    async def face_registrate(self, face_img: UploadFile) -> FaceUser:
        img = self.load_image_into_numpy_array(await face_img.read())

        embedding = await self.embedding_face(img)
        face_user = await self.__user_repo.add_face_user(FaceUser(
            uuid=uuid4(),
            embedding=embedding
        ))
        return face_user

    async def registrate_user(self, user_data: UserPost, face_img: UploadFile):
        face_registrate = await self.face_registrate(face_img)

        user = User(
            uuid=uuid4(),
            login=user_data.login,
            id_type=user_data.id_type,
            id_face_user=face_registrate.id
        )
        user.password = user_data.password

        await self.__user_repo.add(user)

    async def get_user_by_face(self, face_img: UploadFile) -> UserGet:
        img = self.load_image_into_numpy_array(await face_img.read())

        embedding = await self.embedding_face(img)
        face_user_id = await self.__user_repo.get_face_user_by_embedding(embedding)
        user = await self.__user_repo.get_user_by_face_id(face_user_id)
        return UserGet.model_validate(user, from_attributes=True)
