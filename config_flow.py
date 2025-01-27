"""Config Flow for Zonetouch Integration."""
from homeassistant import config_entries
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN  # Import your domain

class ExampleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow for Zonetouch Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # Validate the IP address and port
                cv.ipv4_address(user_input["ip_address"])
                cv.port(user_input["port"])
                
                return self.async_create_entry(title="Example", data=user_input)
            except vol.Invalid:
                errors["base"] = "invalid_input"

        # If no user input or invalid input, show the form again
        data_schema = vol.Schema({
            vol.Required("ip_address"): cv.string,
            vol.Required("port"): cv.port,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

# example_integration.py
#from homeassistant.helpers import config_entry_oauth2_flow

#async def async_setup_entry(hass, entry):
#    """Set up Example integration from a config entry."""
#    # Access the stored data
#    ip_address = entry.data["ip_address"]
#    port = entry.data["port"]#

## Use the IP address and port for your integration setup
#    hass.data[DOMAIN] = {
#        "ip_address": ip_address,
#        "port": port,
#    }
#
#    return True
