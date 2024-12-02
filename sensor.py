import logging

from .const import DOMAIN, SENSOR_TYPES

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import Entity
from homeassistant.const import UnitOfTemperature, UnitOfPressure, UnitOfSpeed


_LOGGER = logging.getLogger(__name__)

def clean_device_id(device_id):
    """Clean device ID to make it stable."""
    return device_id.replace(" ", "_").lower()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up WeatherXM sensors from a config entry."""
    _LOGGER.debug(f"Setting up WeatherXM sensors for entry: {entry.unique_id}")

    api_client = hass.data[DOMAIN].get("api_client")
    if not api_client:
        _LOGGER.error("API client not initialized")
        return

    device_id = clean_device_id(f"{entry.data['deviceId']}_{entry.data['index']}")
    device_name = entry.data["name"]

    sensors = []
    for sensor_type in SENSOR_TYPES:
        sensors.append(
            WeatherXMSensor(
                device_id=device_id,
                device_name=device_name,
                sensor_type=sensor_type,
                unique_id=f"{device_id}_{sensor_type}",
                api_client=api_client,
            )
        )
    async_add_entities(sensors, update_before_add=True)


class WeatherXMSensor(Entity):
    """Representation of a WeatherXM sensor."""

    def __init__(self, device_id, device_name, sensor_type, unique_id, api_client):
        """Initialize the sensor."""
        self.device_id = device_id
        self.device_name = device_name
        self.sensor_type = sensor_type
        self._unique_id = unique_id
        self.api_client = api_client
        self._state = None
        self._attributes = {}

    @property
    def unique_id(self):
        """Return the unique ID for the sensor."""
        return self._unique_id

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.device_id)},
            "name": self.device_name,
            "manufacturer": "WeatherXM",
            "model": "Weather Station",
            "entry_type": DeviceEntryType.SERVICE,  # DeviceEntryType korrekt verwendet
        }

    @property
    def name(self):
        """Return the name of the sensor."""
        sensor_info = SENSOR_TYPES.get(self.sensor_type, {})
        return f"{self.device_name} {sensor_info.get('description', self.sensor_type)}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return self._attributes

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity."""
        return SENSOR_TYPES[self.sensor_type]["unit"]

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return SENSOR_TYPES[self.sensor_type]["icon"]

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            data = await self.api_client.get_sensor_data(self.device_id.split("_")[1], self.device_id.split("_")[0])
            if data and "current_weather" in data:
                weather_data = data["current_weather"]
                sensor_value = weather_data.get(self.sensor_type)
                
                if sensor_value is not None:
                    self._state = sensor_value
                    self._attributes = {
                        "unit": SENSOR_TYPES[self.sensor_type]["unit"],
                        "description": SENSOR_TYPES[self.sensor_type]["description"],
                        "last_updated": weather_data.get("timestamp"),
                    }
                    _LOGGER.debug(f"Updated {self.name}: {self._state} {self._attributes}")
                else:
                    _LOGGER.error(f"Sensor type {self.sensor_type} not found in current_weather data")
            else:
                _LOGGER.error(f"No valid data returned for {self.name}")
        except Exception as e:
            _LOGGER.error(f"Failed to update sensor {self.name}: {e}")