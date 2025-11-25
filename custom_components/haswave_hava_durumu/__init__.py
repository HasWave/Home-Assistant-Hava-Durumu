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
    
    api_url = entry.data.get("api_url", "https://api.haswave.com/api/v1/hava-durumu")
    city = entry.data.get("city")
    district = entry.data.get("district")
    
    # İl/İlçe belirtilmediyse, Home Assistant konumunu kullan
    if not city:
        latitude = hass.config.latitude
        longitude = hass.config.longitude
        _LOGGER.info(f"İl/İlçe belirtilmedi, Home Assistant konumu kullanılıyor: {latitude}, {longitude}")
    else:
        latitude = None
        longitude = None
        _LOGGER.info(f"İl/İlçe bilgisi kullanılıyor. İl: {city}, İlçe: {district or 'Belirtilmedi'}")
    
    timezone = entry.data.get("timezone", hass.config.time_zone or "Europe/Istanbul")
    
    api = HasWaveHavaDurumuAPI(
        api_url=api_url,
        city=city,
        district=district,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        forecast_days=entry.data.get("forecast_days", 7),
    )
    
    update_interval = entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL)
    
    async def async_update_data():
        """Fetch data from API."""
        try:
            data = await hass.async_add_executor_job(api.fetch_weather_data)
            if data:
                _LOGGER.debug(f"API'den hava durumu verisi alındı")
            else:
                _LOGGER.warning("API'den veri alınamadı")
            return data
        except Exception as err:
            _LOGGER.error(f"Veri güncelleme hatası: {err}")
            raise
    
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(seconds=update_interval),
    )
    
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception as err:
        _LOGGER.error(f"İlk veri yükleme hatası: {err}")
        # Hata olsa bile devam et, sensor'lar oluşturulsun
    
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

