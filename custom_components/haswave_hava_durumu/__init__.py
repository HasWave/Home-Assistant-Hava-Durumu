"""The HasWave Hava Durumu integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .api import HasWaveHavaDurumuAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.WEATHER]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HasWave Hava Durumu from a config entry."""
    
    latitude = entry.data.get("latitude")
    longitude = entry.data.get("longitude")
    
    # Eğer konum yoksa, Home Assistant'tan al
    if not latitude or not longitude:
        latitude = hass.config.latitude
        longitude = hass.config.longitude
        timezone = hass.config.time_zone
    else:
        timezone = entry.data.get("timezone", "Europe/Istanbul")
    
    api = HasWaveHavaDurumuAPI(
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        forecast_days=entry.data.get("forecast_days", 7),
    )
    
    update_interval = entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL)
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=api.fetch_weather_data,
        update_interval=timedelta(seconds=update_interval),
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "api": api,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok

