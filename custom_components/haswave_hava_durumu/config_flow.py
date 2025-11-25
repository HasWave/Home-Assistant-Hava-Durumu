"""Config flow for HasWave Hava Durumu integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, DEFAULT_FORECAST_DAYS
from .api import HasWaveHavaDurumuAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional("api_url", default="https://api.haswave.com/api/v1/hava-durumu"): str,
        vol.Optional("city"): str,  # İl adı
        vol.Optional("district"): str,  # İlçe adı (opsiyonel)
        vol.Optional("latitude"): vol.Coerce(float),  # Koordinat için
        vol.Optional("longitude"): vol.Coerce(float),  # Koordinat için
        vol.Optional("timezone", default="Europe/Istanbul"): str,
        vol.Optional("forecast_days", default=DEFAULT_FORECAST_DAYS): int,
        vol.Optional("update_interval", default=DEFAULT_UPDATE_INTERVAL): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api_url = data.get("api_url", "https://api.haswave.com/api/v1/hava-durumu")
    city = data.get("city")
    district = data.get("district")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    
    # Eğer koordinat yoksa ve şehir de yoksa, Home Assistant'tan al
    if not latitude or not longitude:
        if not city:
            latitude = hass.config.latitude
            longitude = hass.config.longitude
            _LOGGER.info(f"Koordinat bilgisi yok, Home Assistant konumu kullanılıyor: {latitude}, {longitude}")
        else:
            latitude = None
            longitude = None
            _LOGGER.info(f"İl/İlçe bilgisi kullanılacak. İl: {city}, İlçe: {district or 'Belirtilmedi'}")
    else:
        _LOGGER.info(f"Koordinat bilgisi kullanılacak: {latitude}, {longitude}")
    
    api = HasWaveHavaDurumuAPI(
        api_url=api_url,
        city=city,
        district=district,
        latitude=latitude,
        longitude=longitude,
        timezone=data.get("timezone", "Europe/Istanbul"),
        forecast_days=data.get("forecast_days", DEFAULT_FORECAST_DAYS),
    )
    
    result = await hass.async_add_executor_job(api.fetch_weather_data)
    
    if not result:
        _LOGGER.error("API'den veri alınamadı")
        raise CannotConnect
    
    # Veri kontrolü
    if not result.get('current') and not result.get('daily'):
        _LOGGER.error("API'den boş veri döndü (hem current hem daily boş)")
        raise CannotConnect
    
    # Başlık oluştur
    if city:
        title = f"HasWave Hava Durumu - {city}"
        if district:
            title += f" / {district}"
    else:
        title = f"HasWave Hava Durumu - {latitude:.2f}, {longitude:.2f}"
    
    return {"title": title}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HasWave Hava Durumu."""
    
    VERSION = 1
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        
        errors = {}
        
        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)
        
        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

