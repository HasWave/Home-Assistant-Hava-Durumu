"""Weather platform for HasWave Hava Durumu."""
from __future__ import annotations

from typing import Any

from homeassistant.components.weather import WeatherEntity, Forecast
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator

from .const import DOMAIN, WMO_TO_HA_CONDITION


def wmo_to_condition(wmo_code: int, precipitation: float = 0, snowfall: float = 0) -> str:
    """Convert WMO weather code to Home Assistant condition."""
    base_condition = WMO_TO_HA_CONDITION.get(wmo_code, 'unknown')
    
    if precipitation > 0 and snowfall > 0:
        return 'snowy-rainy'
    
    return base_condition


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the weather platform."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    async_add_entities([HasWaveHavaDurumuWeather(coordinator)])


class HasWaveHavaDurumuWeather(CoordinatorEntity, WeatherEntity):
    """Representation of a HasWave Hava Durumu weather entity."""
    
    def __init__(self, coordinator: DataUpdateCoordinator) -> None:
        """Initialize the weather entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_weather"
        self._attr_name = "Hava Durumu"
    
    @property
    def condition(self) -> str:
        """Return the current condition."""
        if not self.coordinator.data:
            return 'unknown'
        
        current = self.coordinator.data.get('current', {})
        code = int(current.get('weather_code', 0))
        precip = float(current.get('precipitation', 0))
        snow = float(current.get('snowfall', 0))
        
        return wmo_to_condition(code, precip, snow)
    
    @property
    def temperature(self) -> float | None:
        """Return the temperature."""
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get('current', {}).get('temperature_2m', 0))
    
    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement."""
        return "°C"
    
    @property
    def humidity(self) -> int | None:
        """Return the humidity."""
        if not self.coordinator.data:
            return None
        return int(self.coordinator.data.get('current', {}).get('relative_humidity_2m', 0))
    
    @property
    def pressure(self) -> float | None:
        """Return the pressure."""
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get('current', {}).get('pressure_msl', 0))
    
    @property
    def wind_speed(self) -> float | None:
        """Return the wind speed."""
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get('current', {}).get('wind_speed_10m', 0))
    
    @property
    def wind_bearing(self) -> int | None:
        """Return the wind bearing."""
        if not self.coordinator.data:
            return None
        return int(self.coordinator.data.get('current', {}).get('wind_direction_10m', 0))
    
    @property
    def forecast(self) -> list[Forecast] | None:
        """Return the forecast."""
        if not self.coordinator.data:
            return None
        
        daily = self.coordinator.data.get('daily', {})
        times = daily.get('time', [])
        max_temps = daily.get('temperature_2m_max', [])
        min_temps = daily.get('temperature_2m_min', [])
        codes = daily.get('weather_code', [])
        precip = daily.get('precipitation_sum', [])
        snow = daily.get('snowfall_sum', [])
        
        forecast = []
        for i in range(min(len(times), 7)):
            code = int(codes[i]) if i < len(codes) else 0
            p = float(precip[i]) if i < len(precip) else 0
            s = float(snow[i]) if i < len(snow) else 0
            
            forecast.append({
                'datetime': times[i],
                'condition': wmo_to_condition(code, p, s),
                'temperature': float(max_temps[i]) if i < len(max_temps) else None,
                'templow': float(min_temps[i]) if i < len(min_temps) else None,
                'precipitation': p if p > 0 else None,
            })
        
        return forecast

