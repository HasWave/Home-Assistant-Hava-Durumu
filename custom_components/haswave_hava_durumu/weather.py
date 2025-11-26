"""Weather platform for HasWave Hava Durumu."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.weather import (
    WeatherEntity,
    Forecast,
    WeatherEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN, WMO_TO_HA_CONDITION

_LOGGER = logging.getLogger(__name__)


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
    
    async_add_entities([HasWaveHavaDurumuWeather(coordinator, entry.entry_id)])


class HasWaveHavaDurumuWeather(CoordinatorEntity, WeatherEntity):
    """Representation of a HasWave Hava Durumu weather entity."""
    
    def __init__(self, coordinator: DataUpdateCoordinator, entry_id: str) -> None:
        """Initialize the weather entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_weather"
        # Entity ID'yi sabitlemek için name'i boş bırak veya domain kullan
        # Entity registry entity ID'yi unique_id'den oluşturur
        self._attr_name = "Hava Durumu"
        # Weather-forecast kartı için gerekli özellikler
        self._attr_supported_features = WeatherEntityFeature.FORECAST_DAILY
        # Entity ID'yi manuel olarak ayarla (opsiyonel - entity registry otomatik oluşturur)
        # self.entity_id = f"weather.{DOMAIN}"
    
    @property
    def condition(self) -> str:
        """Return the current condition."""
        if not self.coordinator.data:
            return 'unknown'
        
        current = self.coordinator.data.get('current', {})
        code = int(current.get('weather_code', 0))
        precip = float(current.get('precipitation', 0))
        snow = float(current.get('snowfall', 0))
        
        condition = wmo_to_condition(code, precip, snow)
        _LOGGER.debug(f"Condition: weather_code={code}, precipitation={precip}, snowfall={snow}, condition={condition}")
        
        return condition
    
    @property
    def temperature(self) -> float | None:
        """Return the temperature."""
        if not self.coordinator.data:
            _LOGGER.debug("Temperature: Coordinator data is None")
            return None
        current = self.coordinator.data.get('current', {})
        if not current:
            _LOGGER.warning("Temperature: 'current' key not found or empty")
            return None
        temp = current.get('temperature_2m')
        if temp is None:
            _LOGGER.warning(f"Temperature: 'temperature_2m' is None. Current keys: {list(current.keys())}")
            return None
        try:
            temp_float = float(temp)
            _LOGGER.debug(f"Temperature: {temp_float}°C")
            return temp_float
        except (ValueError, TypeError) as e:
            _LOGGER.warning(f"Temperature: Error converting {temp} to float: {e}")
            return None
    
    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement."""
        return "°C"
    
    @property
    def humidity(self) -> int | None:
        """Return the humidity."""
        if not self.coordinator.data:
            return None
        current = self.coordinator.data.get('current', {})
        if not current:
            return None
        humidity = current.get('relative_humidity_2m')
        if humidity is None:
            return None
        try:
            return int(humidity)
        except (ValueError, TypeError):
            return None
    
    @property
    def pressure(self) -> float | None:
        """Return the pressure."""
        if not self.coordinator.data:
            return None
        current = self.coordinator.data.get('current', {})
        if not current:
            return None
        pressure = current.get('pressure_msl')
        if pressure is None:
            return None
        try:
            return float(pressure)
        except (ValueError, TypeError):
            return None
    
    @property
    def wind_speed(self) -> float | None:
        """Return the wind speed."""
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get('current', {}).get('wind_speed_10m', 0))
    
    @property
    def wind_speed_unit(self) -> str:
        """Return the unit of measurement for wind speed."""
        return "km/h"
    
    @property
    def wind_bearing(self) -> int | None:
        """Return the wind bearing."""
        if not self.coordinator.data:
            return None
        return int(self.coordinator.data.get('current', {}).get('wind_direction_10m', 0))
    
    @property
    def apparent_temperature(self) -> float | None:
        """Return the apparent temperature (hissedilen sıcaklık)."""
        if not self.coordinator.data:
            return None
        return float(self.coordinator.data.get('current', {}).get('apparent_temperature', 0))
    
    async def async_forecast_daily(self) -> list[Forecast] | None:
        """Return the daily forecast."""
        return self._get_forecast()
    
    def _get_forecast(self) -> list[Forecast] | None:
        """Return the forecast (internal method)."""
        if not self.coordinator.data:
            _LOGGER.debug("Forecast: Coordinator data is None")
            return None
        
        # API'den gelen veri formatını kontrol et
        _LOGGER.debug(f"Forecast: Coordinator data keys: {list(self.coordinator.data.keys())}")
        
        daily = self.coordinator.data.get('daily', {})
        if not daily:
            _LOGGER.warning("Forecast: 'daily' key not found in coordinator data")
            return None
        
        times = daily.get('time', [])
        max_temps = daily.get('temperature_2m_max', [])
        min_temps = daily.get('temperature_2m_min', [])
        codes = daily.get('weather_code', [])
        precip = daily.get('precipitation_sum', [])
        snow = daily.get('snowfall_sum', [])
        precip_prob = daily.get('precipitation_probability_max', [])
        
        _LOGGER.debug(f"Forecast: Found {len(times)} days of forecast data")
        
        if not times:
            _LOGGER.warning("Forecast: No time data found in daily forecast")
            return None
        
        forecast = []
        for i in range(min(len(times), 7)):
            try:
                code = int(codes[i]) if i < len(codes) and codes[i] is not None else 0
                p = float(precip[i]) if i < len(precip) and precip[i] is not None else 0.0
                s = float(snow[i]) if i < len(snow) and snow[i] is not None else 0.0
                prob = float(precip_prob[i]) if i < len(precip_prob) and precip_prob[i] is not None else None
                
                # Tarih string'ini datetime objesine çevir
                time_str = times[i]
                if not time_str:
                    _LOGGER.warning(f"Forecast: Empty time string at index {i}")
                    continue
                
                try:
                    # "2025-11-25" formatı
                    if isinstance(time_str, str):
                        dt = datetime.strptime(time_str, "%Y-%m-%d")
                        # Timezone-aware yap (local timezone)
                        dt = dt_util.as_local(dt)
                    else:
                        dt = time_str
                except (ValueError, TypeError) as e:
                    _LOGGER.warning(f"Forecast: Tarih parse hatası: {time_str}, Hata: {e}")
                    continue
                
                max_temp = float(max_temps[i]) if i < len(max_temps) and max_temps[i] is not None else None
                min_temp = float(min_temps[i]) if i < len(min_temps) and min_temps[i] is not None else None
                
                forecast_item: Forecast = {
                    'datetime': dt,
                    'condition': wmo_to_condition(code, p, s),
                    'temperature': max_temp,
                    'templow': min_temp,
                    'precipitation': p if p > 0 else None,
                    'precipitation_probability': int(prob) if prob is not None else None,
                }
                
                forecast.append(forecast_item)
                _LOGGER.debug(f"Forecast: Added day {i+1}: {time_str}, {max_temp}°/{min_temp}°, {forecast_item['condition']}")
                
            except (IndexError, ValueError, TypeError) as e:
                _LOGGER.warning(f"Forecast: Error processing day {i}: {e}")
                continue
        
        _LOGGER.debug(f"Forecast: Returning {len(forecast)} forecast items")
        return forecast if forecast else None
    
    @property
    def forecast(self) -> list[Forecast] | None:
        """Return the forecast (legacy property for compatibility)."""
        return self._get_forecast()

