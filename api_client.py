import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

class WeatherXMApiClient:
    """Client to interact with the WeatherXM API."""

    BASE_URL = "https://api.weatherxm.com/api/v1"

    async def get_sensor_data(self, index, device_id):
        """Fetch sensor data from the API."""
        url = f"{self.BASE_URL}/cells/{index}/devices/{device_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 404:
                        _LOGGER.error(f"Device not found: {url}")
                        return None
                    if response.status != 200:
                        _LOGGER.error(f"Failed to fetch sensor data: {response.status}")
                        return None
                    
                    # Logge die Antwort für Debugging
                    data = await response.json()
                    _LOGGER.debug(f"API response for {device_id}: {data}")
                    return data
            except Exception as e:
                _LOGGER.error(f"Error fetching sensor data: {e}")
                return None

