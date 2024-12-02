import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import re
import aiohttp
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def clean_device_id(device_id):
    """Clean device ID to make it stable."""
    return re.sub(r'\W+', '_', device_id).lower()

class WeatherXMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WeatherXM."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            index = user_input["index"]
            device_id = user_input["deviceId"]

            # Clean the device ID
            cleaned_device_id = clean_device_id(device_id)

            # Set unique ID
            await self.async_set_unique_id(cleaned_device_id)
            self._abort_if_unique_id_configured()

            # Get device name from API
            device_name = await self._get_device_name(index, device_id)
            if not device_name:
                errors["base"] = "cannot_fetch_device_name"
            else:
                return self.async_create_entry(
                    title=device_name,
                    data={
                        "deviceId": device_id,
                        "index": index,
                        "name": device_name,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("deviceId"): str,
                vol.Required("index"): str,
            }),
            errors=errors,
        )

    async def _get_device_name(self, index, device_id):
        """Fetch device name from API."""
        url = f"https://api.weatherxm.com/api/v1/cells/{index}/devices/{device_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        _LOGGER.error(f"Failed to fetch device name, status: {response.status}")
                        return None
                    data = await response.json()
                    return data.get("name")
            except Exception as e:
                _LOGGER.error(f"Error fetching device name: {e}")
                return None
