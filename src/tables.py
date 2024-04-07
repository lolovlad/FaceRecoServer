from sqlalchemy import Column, Integer, String, Date, ForeignKey, UUID, Numeric, Text

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import MutableDict

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

base = declarative_base()


class TypeUser(base):
    __tablename__ = "type_user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(128), nullable=True)


class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4())

    login = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    id_type = Column(Integer, ForeignKey("type_user.id"))
    type = relationship("TypeUser", lazy="joined")
    id_face_user = Column(Integer, ForeignKey("face_user.id"), nullable=True, default=None)
    face_user = relationship("FaceUser", lazy="joined")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class FaceUser(base):
    __tablename__ = "face_user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4())
    embedding = Column(ARRAY(Numeric), nullable=False)


class DiseaseHistory(base):
    __tablename__ = "disease_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, unique=True, default=uuid4())
    id_user = Column(Integer, ForeignKey("user.id"))
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, default=datetime.now())

