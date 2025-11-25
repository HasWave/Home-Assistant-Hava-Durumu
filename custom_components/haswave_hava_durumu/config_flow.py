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
        vol.Optional("latitude"): vol.Coerce(float),
        vol.Optional("longitude"): vol.Coerce(float),
        vol.Optional("timezone", default="Europe/Istanbul"): str,
        vol.Optional("forecast_days", default=DEFAULT_FORECAST_DAYS): int,
        vol.Optional("update_interval", default=DEFAULT_UPDATE_INTERVAL): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    
    if not latitude or not longitude:
        latitude = hass.config.latitude
        longitude = hass.config.longitude
    
    api = HasWaveHavaDurumuAPI(
        latitude=latitude,
        longitude=longitude,
        timezone=data.get("timezone", "Europe/Istanbul"),
        forecast_days=data.get("forecast_days", DEFAULT_FORECAST_DAYS),
    )
    
    result = await hass.async_add_executor_job(api.fetch_weather_data)
    
    if not result:
        raise CannotConnect
    
    return {"title": "HasWave Hava Durumu"}


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

