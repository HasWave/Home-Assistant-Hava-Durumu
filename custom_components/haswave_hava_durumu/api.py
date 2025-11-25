"""API client for HasWave Hava Durumu."""
from __future__ import annotations

import logging
from typing import Any
import requests

from .const import DEFAULT_API_URL

_LOGGER = logging.getLogger(__name__)


class HasWaveHavaDurumuAPI:
    """API client for HasWave Hava Durumu."""
    
    def __init__(self, latitude: float, longitude: float, timezone: str, forecast_days: int = 7) -> None:
        """Initialize the API client."""
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.forecast_days = forecast_days
    
    def fetch_weather_data(self) -> dict[str, Any] | None:
        """Fetch weather data from Open-Meteo API."""
        try:
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'timezone': self.timezone,
                'forecast_days': self.forecast_days,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,snowfall_sum,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant'
            }
            
            response = requests.get(DEFAULT_API_URL, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                _LOGGER.debug(f"API response keys: {list(data.keys())}")
                if 'daily' in data:
                    _LOGGER.debug(f"Daily forecast keys: {list(data['daily'].keys())}")
                    _LOGGER.debug(f"Daily time count: {len(data['daily'].get('time', []))}")
                return data
            else:
                _LOGGER.error(f"HTTP hatası: {response.status_code}")
                _LOGGER.error(f"Response: {response.text[:200]}")
                
        except Exception as e:
            _LOGGER.error(f"API bağlantı hatası: {e}")
        
        return None

