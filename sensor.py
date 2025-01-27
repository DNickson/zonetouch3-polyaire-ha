"""Platform for sensor integration."""
from __future__ import annotations

import logging
from pprint import pformat
import time
from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_ENTITIES, CONF_IP_ADDRESS, CONF_NAME, CONF_PORT

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv

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

    add_entities(
            [
                ZonetouchSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}),
                ZonetouchStaticSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}, "System Name"),
                ZonetouchStaticSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}, "System ID"),
                ZonetouchStaticSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}, "Installer Name"),
                ZonetouchStaticSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}, "Installer Number"),
                ZonetouchStaticSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}, "Firmware Version"),
                ZonetouchStaticSensor({"name": config[CONF_NAME],"address": config[CONF_IP_ADDRESS],"port": config[CONF_PORT],"zone": 0}, "Console Version")
            ]
        )

class ZonetouchStaticSensor(SensorEntity):
    def __init__(self, sensor, name):
        self._sensor = Zonetouch3(sensor["address"], sensor["port"], sensor["zone"])
        self._attr_name = name
        self._attr_unique_id = 'ZT3' + self._attr_name
        self._attr_native_value = self.fetch_data()

    def fetch_data(self):
        if self._attr_name == "System Name":
            return self.fetch_system_name(self)
        elif self._attr_name == "System ID":
            return self.fetch_system_id(self)
        elif self._attr_name == "Installer Name":
            return self.fetch_installer_name(self)
        elif self._attr_name == "Installer Number":
            return self.fetch_installer_number(self)
        elif self._attr_name == "Firmware Version":
            return self.fetch_system_firmware(self)
        elif self._attr_name == "Console Version":
            return self.fetch_console_version(self)
        else:
            return None

    @staticmethod
    def fetch_system_name(self):
        return self._sensor.get_zonetouch_system_name()

    @staticmethod
    def fetch_system_id(self):
        return self._sensor.get_zonetouch_system_id()

    @staticmethod
    def fetch_installer_name(self):
        return self._sensor.get_zonetouch_system_installer()

    @staticmethod
    def fetch_installer_number(self):
        return self._sensor.get_zonetouch_system_installer_number()
    
    @staticmethod
    def fetch_system_firmware(self):
        return self._sensor.get_zonetouch_system_firmware()
    
    @staticmethod
    def fetch_console_version(self):
        return self._sensor.get_zonetouch_console_version()
    
    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self.fetch_data()

class ZonetouchSensor(SensorEntity):
    """Monitor Zonetouch Sensor"""
    
    def __init__(self, sensor) -> None:
        self._sensor = Zonetouch3(sensor["address"], sensor["port"], sensor["zone"])
        self._attr_name = "Zonetouch Console Temperature"
        self._attr_unique_id = 'ZT3' + self._attr_name
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_value = self._sensor.get_zonetouch_temp()

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = self._sensor.get_zonetouch_temp()