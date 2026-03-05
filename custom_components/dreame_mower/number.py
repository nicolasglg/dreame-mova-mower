"""Support for Dreame Mower numbers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from homeassistant.components.number import (
    ENTITY_ID_FORMAT,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, UNIT_PERCENT

from .coordinator import DreameMowerDataUpdateCoordinator
from .entity import DreameMowerEntity, DreameMowerEntityDescription
from .dreame import DreameMowerAction, DreameMowerProperty

@dataclass
class DreameMowerNumberEntityDescription(DreameMowerEntityDescription, NumberEntityDescription):
    """Describes Dreame Mower Number entity."""

    mode: NumberMode = NumberMode.AUTO
    post_action: DreameMowerAction = None
    set_fn: Callable[[object, int]] = None
    max_value_fn: Callable[[object], int] = None
    min_value_fn: Callable[[object], int] = None


NUMBERS: tuple[DreameMowerNumberEntityDescription, ...] = (
    DreameMowerNumberEntityDescription(
        property_key=DreameMowerProperty.VOLUME,
        icon_fn=lambda value, device: "mdi:volume-off" if value == 0 else "mdi:volume-high",
        mode=NumberMode.SLIDER,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=UNIT_PERCENT,
        entity_category=EntityCategory.CONFIG,
        post_action=DreameMowerAction.TEST_SOUND,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Dreame Mower number based on a config entry."""
    coordinator: DreameMowerDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        DreameMowerNumberEntity(coordinator, description)
        for description in NUMBERS
        if description.exists_fn(description, coordinator.device)
    )


class DreameMowerNumberEntity(DreameMowerEntity, NumberEntity):
    """Defines a Dreame Mower number."""

    def __init__(
        self,
        coordinator: DreameMowerDataUpdateCoordinator,
        description: DreameMowerNumberEntityDescription,
    ) -> None:
        """Initialize Dreame Mower number."""
        if description.set_fn is None and (description.property_key is not None or description.key is not None):
            if description.property_key is not None:
                prop = f"set_{description.property_key.name.lower()}"
            else:
                prop = f"set_{description.key.lower()}"
            if hasattr(coordinator.device, prop):
                description.set_fn = lambda device, value: getattr(device, prop)(value)

        if description.min_value_fn:
            description.native_min_value = description.min_value_fn(coordinator.device)
        if description.max_value_fn:
            description.native_max_value = description.max_value_fn(coordinator.device)

        super().__init__(coordinator, description)
        self._generate_entity_id(ENTITY_ID_FORMAT)
        self._attr_mode = description.mode
        self._attr_native_value = super().native_value

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_native_value = super().native_value
        if self.entity_description.min_value_fn:
            self.entity_description.native_min_value = self.entity_description.min_value_fn(self.device)
        if self.entity_description.max_value_fn:
            self.entity_description.native_max_value = self.entity_description.max_value_fn(self.device)
        super()._handle_coordinator_update()

    async def async_set_native_value(self, value: float) -> None:
        """Set the Dreame Mower number value."""
        if not self.available:
            raise HomeAssistantError("Entity unavailable")

        value = int(value)
        if self.entity_description.format_fn is not None:
            value = self.entity_description.format_fn(value, self.device)

        if value is None:
            raise HomeAssistantError("Invalid value")

        result = False

        if self.entity_description.set_fn is not None:
            result = await self._try_command("Unable to call: %s", self.entity_description.set_fn, self.device, value)
        elif self.entity_description.property_key is not None:
            result = await self._try_command(
                "Unable to call: %s",
                self.device.set_property,
                self.entity_description.property_key,
                value,
            )

        if result and self.entity_description.post_action is not None:
            await self._try_command(
                "Unable to call %s",
                self.device.call_action,
                self.entity_description.post_action,
            )

    @property
    def native_value(self) -> int | None:
        """Return the current Dreame Mower number value."""
        return self._attr_native_value
