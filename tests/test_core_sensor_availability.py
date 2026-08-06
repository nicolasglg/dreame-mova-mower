import ast
from pathlib import Path


SENSOR_SOURCE = (
    Path(__file__).parents[1]
    / "custom_components"
    / "dreame_mower"
    / "sensor.py"
)
CORE_PROPERTIES = {"STATE", "CHARGING_STATUS", "BATTERY_LEVEL"}


def test_core_sensors_are_registered_when_initial_discovery_is_partial():
    tree = ast.parse(SENSOR_SOURCE.read_text())
    unconditional = set()

    for call in ast.walk(tree):
        if not isinstance(call, ast.Call):
            continue
        if not isinstance(call.func, ast.Name):
            continue
        if call.func.id != "DreameMowerSensorEntityDescription":
            continue

        keywords = {keyword.arg: keyword.value for keyword in call.keywords}
        property_key = keywords.get("property_key")
        exists_fn = keywords.get("exists_fn")
        if not (
            isinstance(property_key, ast.Attribute)
            and property_key.attr in CORE_PROPERTIES
            and isinstance(exists_fn, ast.Lambda)
            and isinstance(exists_fn.body, ast.Constant)
            and exists_fn.body.value is True
        ):
            continue
        unconditional.add(property_key.attr)

    assert unconditional == CORE_PROPERTIES
