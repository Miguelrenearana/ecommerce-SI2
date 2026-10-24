from enum import Enum


class RolEnum(str, Enum):
    superadmin = "superadmin"
    administrador = "administrador"
    cliente = "cliente"
    proveedor = "proveedor"
    encargado = "encargado"
    cajero = "cajero"
    delivery = "delivery"


class GenderEnum(str, Enum):
    masculino = "masculino"
    femenino = "femenino"


class ProviderStatusEnum(str, Enum):
    active = "active"
    suspended = "suspended"
