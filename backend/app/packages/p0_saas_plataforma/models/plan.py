import uuid
from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False)  # BASICO, PROFESIONAL
    code = Column(String(30), unique=True, nullable=False)  # basic, pro
    description = Column(Text, nullable=True)
    max_branches = Column(Integer, nullable=False, default=2)  # 2 para Básico, 10 para Pro
    has_ai_access = Column(Boolean, nullable=False, default=False)  # False para Básico, True para Pro
    price_monthly = Column(Numeric(10, 2), nullable=False, default=0.0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    subscriptions = relationship("Subscription", back_populates="plan")
