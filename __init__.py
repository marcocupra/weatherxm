import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_registry import async_get
from .api_client import WeatherXMApiClient  # Füge diese Datei mit der API-Logik hinzu.

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the WeatherXM integration."""
    _LOGGER.debug("Setting up WeatherXM integration")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up WeatherXM from a config entry."""
    _LOGGER.debug(f"Setting up WeatherXM entry: {entry.unique_id}")

    # Initialize the API client
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["api_client"] = WeatherXMApiClient()

    # Forward to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug(f"Unloading WeatherXM entry: {entry.unique_id}")

    # Unload platforms
    unloaded = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    # Remove from data storage
    if unloaded and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    # Clean up entity registry
    entity_registry = async_get(hass)
    for entity_id in list(entity_registry.entities):
        entity = entity_registry.entities[entity_id]
        if entity.config_entry_id == entry.entry_id:
            _LOGGER.debug(f"Removing entity: {entity_id}")
            entity_registry.async_remove(entity_id)

    return unloaded

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload a config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
