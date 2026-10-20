import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.packages.p1_gestion_usuarios_acceso.schemas.enums import RolEnum


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(Enum(RolEnum), nullable=False, default=RolEnum.cliente)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, nullable=False, default=True)

    body_profile = relationship("UserBodyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    conversation = relationship("Conversation", back_populates="user", uselist=False, cascade="all, delete-orphan")


# Register related user body profile mapper.
from app.packages.p1_gestion_usuarios_acceso.models.user_profile import UserBodyProfile  # noqa: E402, F401
