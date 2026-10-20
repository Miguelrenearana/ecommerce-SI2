# Re-export from canonical package location for backward compatibility
from app.packages.p1_gestion_usuarios_acceso.schemas.provider_availability_schema import (
    ProviderAvailabilityBatchUpdate,
    ProviderAvailabilityUpdate,
)

__all__ = [
    "ProviderAvailabilityBatchUpdate",
    "ProviderAvailabilityUpdate",
]
