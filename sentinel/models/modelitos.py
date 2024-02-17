import uuid

from sqlalchemy.sql import func
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, Enum, Float, Column, String, DateTime, ForeignKey

from sentinel import __version__
from sentinel.models.base import Base, PrintableBase, UpdatableBase


class ObjA(Base, UpdatableBase, PrintableBase):

    __tablename__ = "obj_a"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    string_a = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        # default=datetime.utcnow,
        server_default=func.now(),  # pylint: disable=not-callable
    )

    objs_a_to_b = relationship("ObjAtoB", back_populates="obj_a")


class ObjAtoB(Base, UpdatableBase, PrintableBase):

    __tablename__ = "objs_a_to_b"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    extra = Column(Float, nullable=False)

    b_id = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        nullable=False,
        # default=datetime.utcnow,
        server_default=func.now(),  # pylint: disable=not-callable
    )

    a_id = Column(UUIDType(binary=False), ForeignKey("obj_a.id"), nullable=False)
    obj_a = relationship("ObjA", back_populates="objs_a_to_b")


class ObjB(Base, UpdatableBase, PrintableBase):
    __tablename__ = "obj_b"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    string_b = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        # default=datetime.utcnow,
        server_default=func.now(),  # pylint: disable=not-callable
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # default=datetime.utcnow,
        server_default=func.now(),  # pylint: disable=not-callable
    )
