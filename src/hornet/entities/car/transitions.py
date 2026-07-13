from hornet.entities.car.car_status import CarStatus

ALLOWED_TRANSITIONS: dict[CarStatus, set[CarStatus]] = {
    CarStatus.available: {CarStatus.in_use, CarStatus.under_maintenance},
    CarStatus.in_use: {CarStatus.available},
    CarStatus.under_maintenance: {CarStatus.available},
}

def can_transition(current: CarStatus, target: CarStatus) -> bool:
    return current == target or target in ALLOWED_TRANSITIONS.get(current, set())
