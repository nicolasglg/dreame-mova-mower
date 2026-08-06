import ast
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from dreame.device import DreameMowerDevice


DEVICE_SOURCE = (
    Path(__file__).parents[1]
    / "custom_components"
    / "dreame_mower"
    / "dreame"
    / "device.py"
)


def _method_calls(method_name: str) -> list[str]:
    tree = ast.parse(DEVICE_SOURCE.read_text())
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == method_name
    )
    return [
        node.func.attr
        for node in ast.walk(method)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    ]


def test_request_current_zone_hydrates_from_dreame_cloud_stored_property():
    device = object.__new__(DreameMowerDevice)
    device.current_zone_id = None
    device.current_zone_state = None
    device._ready = True
    device._update_callback = Mock()
    device._protocol = SimpleNamespace(
        cloud=SimpleNamespace(
            get_properties=Mock(
                return_value=[
                    {
                        "key": "2.56",
                        "value": '{"status":[[1,-1],[2,0],[3,-1]]}',
                        "updateDate": 1786021219628,
                    }
                ]
            )
        )
    )

    device._request_current_zone()

    device._protocol.cloud.get_properties.assert_called_once_with("2.56")
    assert device.current_zone_id == 2
    assert device.current_zone_state == 0
    device._update_callback.assert_called_once_with()


def test_connect_device_hydrates_current_zone_after_initial_properties():
    assert "_request_current_zone" in _method_calls("connect_device")


def test_forced_update_rehydrates_current_zone_after_reconnect():
    assert "_request_current_zone" in _method_calls("update")


def test_current_zone_name_uses_the_name_loaded_from_the_dreame_map():
    device = object.__new__(DreameMowerDevice)
    device.current_zone_id = 2
    device.status = SimpleNamespace(
        current_segments={2: SimpleNamespace(name="Allée")}
    )

    assert device.current_zone_name == "Allée"
