import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Numeric, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Branch(Base):
    __tablename__ = "branches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String(255), nullable=False, default="")
    phone = Column(String(50), nullable=False, default="")
    opening_hours = Column(String(100), nullable=False, default="09:00 - 20:00")
    latitude = Column(Numeric(10, 7), nullable=False, default=-17.7833000)
    longitude = Column(Numeric(10, 7), nullable=False, default=-63.1821000)
    is_default = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)

    company = relationship("Company", foreign_keys=[tenant_id])
