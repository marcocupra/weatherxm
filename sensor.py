import aiohttp
import logging
from datetime import timedelta

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(minutes=5)

async def async_get_weatherxm_data(session, index, device_id):
    url = f"https://api.weatherxm.com/api/v1/cells/{index}/devices/{device_id}"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            _LOGGER.error(f"Failed to fetch data from WeatherXM API, status code: {response.status}")
            return None

class WeatherXMSensor(Entity):
    def __init__(self, index, device_id, sensor_type, device_name, value, unit, icon):
        self.index = index
        self.device_id = device_id
        self.sensor_type = sensor_type
        self._entity_name = f"{device_name}_{sensor_type}"  # Entitäts-ID im Format stationname_sensortyp
        self._state = value
        self._unit_of_measurement = unit
        self._icon = icon
        self._unique_id = f"{index}_{device_id}_{sensor_type}"

        # Deutsche Übersetzungen für die Sensor-Typen (für friendly_name)
        translations = {
            "temperature": "Temperatur",
            "humidity": "Luftfeuchtigkeit",
            "wind_speed": "Windgeschwindigkeit",
            "wind_gust": "Windböen",
            "wind_direction": "Windrichtung",
            "solar_irradiance": "Sonnenstrahlung",
            "uv_index": "UV-Index",
            "precipitation": "Niederschlag",
            "precipitation_accumulated": "Niederschlagsmenge",
            "pressure": "Luftdruck",
            "dew_point": "Taupunkt",
            "feels_like": "Gefühlte Temperatur"
        }

        # Der "friendly_name" zeigt nur die deutsche Übersetzung des Sensortyps an
        self._friendly_name = translations.get(sensor_type, sensor_type)

    @property
    def name(self):
        """Gibt den Entitätsnamen zurück."""
        return self._entity_name  # Entitätsname im Format stationname_sensortyp

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def icon(self):
        return self._icon

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def device_info(self):
        """Informationen über das Gerät, dem der Sensor zugeordnet ist."""
        return {
            "identifiers": {(f"weatherxm_{self.index}_{self.device_id}")},  # Eindeutige Geräte-ID
            "name": "WeatherXM Wetterstation",  # Name des Geräts
            "manufacturer": "WeatherXM",
            "model": "WeatherXM Station",
            "sw_version": "1.0",
        }

    @property
    def extra_state_attributes(self):
        """Gibt zusätzliche Attribute zurück, einschließlich friendly_name."""
        return {
            "friendly_name": self._friendly_name
        }

    async def async_update(self):
        """Ruft die aktuellen Daten von der API ab und aktualisiert den Zustand."""
        session = aiohttp.ClientSession()
        data = await async_get_weatherxm_data(session, self.index, self.device_id)
        await session.close()

        if data:
            self._state = data["current_weather"].get(self.sensor_type)
            _LOGGER.debug(f"Updated {self._entity_name}: {self._state}")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up WeatherXM sensors based on a config entry."""
    _LOGGER.debug(f"Start setup for entry: {entry}")
    index = entry.data["index"]
    device_id = entry.data["deviceId"]

    session = aiohttp.ClientSession()
    data = await async_get_weatherxm_data(session, index, device_id)
    await session.close()

    if not data:
        _LOGGER.error("Keine Daten erhalten, Sensoren werden nicht hinzugefügt.")
        return

    device_name = data.get("name", f"{index}-{device_id}")

    sensor_types = [
        ("temperature", "°C", "mdi:thermometer"),
        ("humidity", "%", "mdi:water-percent"),
        ("wind_speed", "m/s", "mdi:weather-windy"),
        ("wind_gust", "m/s", "mdi:weather-windy"),
        ("wind_direction", "°", "mdi:compass"),
        ("solar_irradiance", "W/m²", "mdi:weather-sunny"),
        ("uv_index", None, "mdi:weather-sunny-alert"),
        ("precipitation", "mm/h", "mdi:weather-rainy"),
        ("precipitation_accumulated", "mm", "mdi:weather-rainy"),
        ("pressure", "hPa", "mdi:gauge"),
        ("dew_point", "°C", "mdi:thermometer"),
        ("feels_like", "°C", "mdi:thermometer"),
    ]

    sensors = [
        WeatherXMSensor(
            index, device_id, sensor_type, device_name,
            data["current_weather"].get(sensor_type), unit, icon
        )
        for sensor_type, unit, icon in sensor_types
    ]

    async_add_entities(sensors, update_before_add=True)

    # Register update interval
    async def update_sensors(event_time):
        for sensor in sensors:
            await sensor.async_update()
            sensor.async_write_ha_state()

    async_track_time_interval(hass, update_sensors, UPDATE_INTERVAL)
