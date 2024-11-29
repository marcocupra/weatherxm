import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
import aiohttp

from .const import DOMAIN

@callback
def configured_instances(hass):
    """Return a set of configured WeatherXM instances."""
    return {entry.data["deviceId"] for entry in hass.config_entries.async_entries(DOMAIN)}

class WeatherXMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WeatherXM."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            if user_input["deviceId"] in configured_instances(self.hass):
                errors["base"] = "device_exists"
            else:
                try:
                    # Hier wird der Gerätename zum entry hinzugefügt
                    device_name = await self._get_device_name(user_input["index"], user_input["deviceId"])
                    user_input["device_name"] = device_name

                    return self.async_create_entry(
                        title=device_name,  # Setze den Gerätenamen als Titel
                        data=user_input
                    )
                except Exception as e:
                    errors["base"] = "cannot_connect"
                    _LOGGER.error(f"Fehler beim Abrufen des Gerätenamens: {e}")

        data_schema = vol.Schema({
            vol.Required("index"): str,
            vol.Required("deviceId"): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    async def _get_device_name(self, index, device_id):
        """Fetch the device name based on the index and device_id."""
        session = aiohttp_client.async_get_clientsession(self.hass)
        url = f"https://api.weatherxm.com/api/v1/cells/{index}/devices/{device_id}"
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception("Fehler beim Abrufen der Geräteinformationen")
            data = await response.json()
            return data.get("name", f"WeatherXM {device_id}")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return WeatherXMOptionsFlowHandler(config_entry)

class WeatherXMOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for WeatherXM."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options for the custom component."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("update_interval_value", default=self.config_entry.options.get("update_interval_value", 5)): int,
            vol.Optional("update_interval_unit", default=self.config_entry.options.get("update_interval_unit", "minutes")): vol.In(["seconds", "minutes", "hours"]),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=options_schema
        )
