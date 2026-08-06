from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from dreame.device import DreameMowerDevice
from dreame.exceptions import InvalidActionException
from dreame.types import DreameMowerStatus


def make_device(model: str = "dreame.mower.g2422") -> DreameMowerDevice:
    device = object.__new__(DreameMowerDevice)
    device.info = SimpleNamespace(model=model)
    device.status = SimpleNamespace(
        current_map=None,
        has_saved_map=True,
        current_segments={},
        customized_cleaning=False,
        started=True,
        paused=False,
    )
    device._map_manager = None
    device._update_status = Mock()
    device._protocol = SimpleNamespace(action=Mock(return_value={"code": 0}))
    device.schedule_update = Mock()
    device.start_custom = Mock()
    return device


def test_a1_pro_zone_mowing_uses_native_mower_task_api():
    device = make_device()

    result = device.clean_segment(1)

    assert result == {"code": 0}
    device._protocol.action.assert_called_once_with(
        2,
        50,
        [{"m": "a", "p": 0, "o": 102, "d": {"region": [1]}}],
    )
    device.start_custom.assert_not_called()
    device.schedule_update.assert_called_once_with(10, True)


def test_a1_pro_zone_mowing_rejects_non_positive_zone_ids():
    device = make_device()

    with pytest.raises(InvalidActionException, match="Invalid A1 Pro zone ids"):
        device.clean_segment(0)

    device._protocol.action.assert_not_called()


def test_a1_pro_zone_mowing_rejects_non_numeric_zone_ids():
    device = make_device()

    with pytest.raises(InvalidActionException, match="Invalid A1 Pro zone ids"):
        device.clean_segment("Jardin")

    device._protocol.action.assert_not_called()


def test_a1_pro_zone_mowing_schedules_fast_refresh_after_api_failure():
    device = make_device()
    device._protocol.action.return_value = None

    result = device.clean_segment(1)

    assert result is None
    assert device.schedule_update.call_args_list == [call(10, True), call(1, True)]


def test_a1_pro_zone_mowing_rejects_nonzero_api_code():
    device = make_device()
    device._protocol.action.return_value = {"code": 500}

    result = device.clean_segment(1)

    assert result is None
    assert device.schedule_update.call_args_list == [call(10, True), call(1, True)]


def test_other_models_keep_legacy_start_custom_segment_flow():
    device = make_device("dreame.mower.other")
    device.start_custom.return_value = {"code": 0}

    result = device.clean_segment(2)

    assert result == {"code": 0}
    device._protocol.action.assert_not_called()
    device.start_custom.assert_called_once_with(
        DreameMowerStatus.SEGMENT_CLEANING.value,
        '{"selects":[[2,1,1]]}',
    )
