import pytest

from hornet.entities import CarStatus, can_transition

@pytest.mark.parametrize(
    "current,target,expected",
    [
        (CarStatus.available, CarStatus.in_use, True),
        (CarStatus.available, CarStatus.under_maintenance, True),
        (CarStatus.available, CarStatus.available, True),
        (CarStatus.in_use, CarStatus.available, True),
        (CarStatus.in_use, CarStatus.in_use, True),
        (CarStatus.in_use, CarStatus.under_maintenance, False),
        (CarStatus.under_maintenance, CarStatus.available, True),
        (CarStatus.under_maintenance, CarStatus.under_maintenance, True),
        (CarStatus.under_maintenance, CarStatus.in_use, False),
    ],
)
def test_can_transition(current, target, expected):
    assert can_transition(current, target) is expected
