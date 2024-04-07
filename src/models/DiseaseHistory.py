from pydantic import BaseModel, UUID4, field_serializer
from datetime import datetime


class DiseaseHistoryBase(BaseModel):
    uuid: UUID4

    @field_serializer('uuid')
    def serialize_uuid(self, uuid: UUID4, _info):
        return str(uuid)


class PostDiseaseHistory(BaseModel):
    uuid_user: str
    name: str
    description: str


class GetDiseaseHistory(DiseaseHistoryBase):
    name: str
    description: str
    date: datetime
