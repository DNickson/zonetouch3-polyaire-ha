"""Platform for light integration."""

from __future__ import annotations

import logging
from pprint import pformat
import time
from typing import Any

import voluptuous as vol

from homeassistant.components.fan import PLATFORM_SCHEMA, FanEntity, FanEntityFeature
from homeassistant.const import CONF_ENTITIES, CONF_IP_ADDRESS, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .zonetouch3 import Zonetouch3

_LOGGER = logging.getLogger("ZoneTouch3")

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default ="zonetouch3"): cv.string,
    vol.Optional(CONF_ENTITIES, default ="8"): cv.positive_int,
    vol.Required(CONF_IP_ADDRESS): cv.string,
    vol.Optional(CONF_PORT, default = 7030): cv.port,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    "Setup the platform"
    _LOGGER.info(pformat(config))

    # loop though zone amount, create/entities objects per zone
    for zone_no in range(0, config[CONF_ENTITIES]):
        add_entities(
            [
                zonetouch_3(
                    {
                        "name": config[CONF_NAME] + "_Zone" + str(zone_no),
                        "address": config[CONF_IP_ADDRESS],
                        "port": config[CONF_PORT],
                        "zone": zone_no,
                    }
                )
            ]
        )

class zonetouch_3(FanEntity):

    _attr_icon = "mdi:air-conditioner"
    _attr_supported_features = (
        FanEntityFeature.SET_SPEED
        | FanEntityFeature.TURN_OFF
        | FanEntityFeature.TURN_ON
    )

    def __init__(self, fan) -> None:
        _LOGGER.info(pformat(fan))

        self.fan = Zonetouch3(fan["address"], fan["port"], fan["zone"])
        self._name = self.fan.get_zone_name()
        self._attr_unique_id = self._name
        self._state = self.fan.get_zone_state()
        self._attr_percentage = self.fan.get_zone_percentage()

        # Getters
    @property
    def name(self) -> str:
        """Return the display name of this fan."""
        return self._name
    
    @property
    def is_on(self) -> bool | None:
        """Return true if the entity is on."""
        return self._state
    
    def turn_on(self, **kwargs: Any) -> None:
        self.fan.update_zone_state('03', 150)
        time.sleep(0.5)
        self.update()
    
    def turn_off(self, **kwargs: Any) -> None:
        self.fan.update_zone_state('02', 150)
        time.sleep(0.5)
        self.update()

    @property
    def percentage(self) -> int | None:
        """Return the current percentage."""
        return self._attr_percentage
    
    def set_percentage(self, percentage: int) -> None:
        self.fan.update_zone_state('80', percentage)
        time.sleep(0.5)
        self.update()
    
    def update(self) -> None:
        """Get live state of individual fan."""
        self._state = self.fan.get_zone_state()
        self._attr_percentage = self.fan.get_zone_percentage()
