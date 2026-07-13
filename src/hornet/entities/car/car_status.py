from enum import StrEnum

class CarStatus(StrEnum):
    available = "available"
    in_use = "in_use"
    under_maintenance = "under_maintenance"
