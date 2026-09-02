from types import SimpleNamespace
from unittest.mock import Mock

from dreame.device import DreameMowerDevice


def make_device(*, docked: bool = False, charging: bool = False, returning: bool = False) -> DreameMowerDevice:
    device = object.__new__(DreameMowerDevice)
    device.current_zone_id = None
    device.current_zone_state = None
    device.status = SimpleNamespace(docked=docked, charging=charging, returning=returning)
    device._update_callback = Mock()
    return device


def _param(status):
    return {"siid": 2, "piid": 56, "value": {"status": status}}


def test_priority_prefers_state_0_over_state_4():
    device = make_device()

    device._update_current_zone(_param([[1, 4], [2, 0], [3, -1]]))

    assert device.current_zone_id == 2
    assert device.current_zone_state == 0


def test_falls_back_to_state_4_when_no_state_0_zone_exists():
    device = make_device()

    device._update_current_zone(_param([[1, -1], [2, 4]]))

    assert device.current_zone_id == 2
    assert device.current_zone_state == 4


def test_resets_current_zone_when_only_pending_zones_remain():
    device = make_device()
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone(_param([[1, -1], [2, -1]]))

    assert device.current_zone_id is None
    assert device.current_zone_state is None
    device._update_callback.assert_called_once_with()


def test_resets_current_zone_when_all_zones_are_completed():
    device = make_device()
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone(_param([[1, 2], [2, 2]]))

    assert device.current_zone_id is None
    assert device.current_zone_state is None


def test_ignores_zone_updates_while_docked():
    device = make_device(docked=True)
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone(_param([[1, 0], [2, -1]]))

    assert device.current_zone_id is None
    assert device.current_zone_state is None


def test_ignores_zone_updates_while_charging():
    device = make_device(charging=True)
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone(_param([[1, 0]]))

    assert device.current_zone_id is None
    assert device.current_zone_state is None


def test_ignores_zone_updates_while_returning_to_base():
    device = make_device(returning=True)
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone(_param([[1, 0]]))

    assert device.current_zone_id is None
    assert device.current_zone_state is None


def test_ignores_malformed_zone_payload():
    device = make_device()
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone({"siid": 2, "piid": 56, "value": {"status": "not-a-list"}})

    assert device.current_zone_id == 1
    assert device.current_zone_state == 0
    device._update_callback.assert_not_called()


def test_ignores_absent_zone_payload():
    device = make_device()
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone({"siid": 2, "piid": 56, "value": None})

    assert device.current_zone_id == 1
    assert device.current_zone_state == 0
    device._update_callback.assert_not_called()


def test_ignores_unrelated_property():
    device = make_device()
    device.current_zone_id = 1
    device.current_zone_state = 0

    device._update_current_zone({"siid": 2, "piid": 1, "value": {"status": [[1, 0]]}})

    assert device.current_zone_id == 1
    assert device.current_zone_state == 0
    device._update_callback.assert_not_called()
