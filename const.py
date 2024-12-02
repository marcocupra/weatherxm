from homeassistant.const import (
    UnitOfTemperature,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfIrradiance,
    UnitOfPrecipitationDepth,
)

DOMAIN = "weatherxm"

# Definiere die Sensortypen mit ihren Einheiten und Beschreibungen
SENSOR_TYPES = {
    "temperature": {"unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer", "description": "Temperature"},
    "humidity": {"unit": "%", "icon": "mdi:water-percent", "description": "Humidity"},
    "wind_speed": {"unit": UnitOfSpeed.METERS_PER_SECOND, "icon": "mdi:weather-windy", "description": "Wind Speed"},
    "wind_gust": {"unit": UnitOfSpeed.METERS_PER_SECOND, "icon": "mdi:weather-windy", "description": "Wind Gust"},
    "wind_direction": {"unit": "°", "icon": "mdi:compass", "description": "Wind Direction"},
    "solar_irradiance": {"unit": UnitOfIrradiance.WATTS_PER_SQUARE_METER, "icon": "mdi:weather-sunny", "description": "Solar Irradiance"},
    "uv_index": {"unit": None, "icon": "mdi:weather-sunny-alert", "description": "UV Index"},
    "precipitation": {"unit": "mm/h", "icon": "mdi:weather-rainy", "description": "Precipitation"},
    "precipitation_accumulated": {"unit": UnitOfPrecipitationDepth.MILLIMETERS, "icon": "mdi:weather-rainy", "description": "Accumulated Precipitation"},
    "pressure": {"unit": UnitOfPressure.HPA, "icon": "mdi:gauge", "description": "Pressure"},
    "dew_point": {"unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer", "description": "Dew Point"},
    "feels_like": {"unit": UnitOfTemperature.CELSIUS, "icon": "mdi:thermometer", "description": "Feels Like"},
}
