import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(150), nullable=False)
    business_name = Column(String(200), nullable=False)
    nit_rut = Column(String(50), unique=True, index=True, nullable=False)
    subdomain = Column(String(63), unique=True, index=True, nullable=False)
    status = Column(String(20), nullable=False, default="ACTIVO")  # ACTIVO, SUSPENDIDO
    email = Column(String(120), nullable=True)
    phone = Column(String(30), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    subscriptions = relationship(
        "Subscription",
        back_populates="company",
        cascade="all, delete-orphan",
        order_by="desc(Subscription.start_date)",
    )
