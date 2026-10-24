import uuid
from sqlalchemy import Boolean, Column, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(50), unique=True, nullable=False)  # BASICO, PROFESIONAL
    code = Column(String(30), unique=True, nullable=False)  # basic, pro
    max_branches = Column(Integer, nullable=False, default=2)  # 2 para Básico, 10 para Pro
    has_ai_access = Column(Boolean, nullable=False, default=False)  # False para Básico, True para Pro
    price_monthly = Column(Numeric(10, 2), nullable=False, default=0.0)
    is_active = Column(Boolean, nullable=False, default=True)

    subscriptions = relationship("Subscription", back_populates="plan")
