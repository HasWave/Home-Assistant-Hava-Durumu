"""API client for HasWave Hava Durumu."""
from __future__ import annotations

import logging
from typing import Any
import requests

from .const import DEFAULT_API_URL

_LOGGER = logging.getLogger(__name__)


class HasWaveHavaDurumuAPI:
    """API client for HasWave Hava Durumu."""
    
    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        city: str | None = None,
        district: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        timezone: str = "Europe/Istanbul",
        forecast_days: int = 7
    ) -> None:
        """Initialize the API client."""
        self.api_url = api_url
        self.city = city
        self.district = district
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.forecast_days = forecast_days
    
    def fetch_weather_data(self) -> dict[str, Any] | None:
        """Fetch weather data from HasWave API."""
        try:
            params = {}
            
            # İl/İlçe parametreleri
            if self.city:
                params['il'] = self.city
            if self.district:
                params['ilce'] = self.district
            
            # Open-Meteo için koordinat parametreleri
            if self.latitude and self.longitude:
                params['latitude'] = self.latitude
                params['longitude'] = self.longitude
            
            # Diğer parametreler
            if self.timezone:
                params['timezone'] = self.timezone
            if self.forecast_days:
                params['forecast_days'] = self.forecast_days
            
            _LOGGER.debug(f"API isteği: {self.api_url} - Params: {params}")
            
            response = requests.get(self.api_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # API response formatını kontrol et
                if data.get('success', True):
                    # HasWave API formatı (success: true, data: {...})
                    weather_data = data.get('data', data)
                    
                    # Veri kontrolü
                    if not weather_data:
                        _LOGGER.error("API'den boş veri döndü")
                        return None
                    
                    _LOGGER.debug(f"API response keys: {list(weather_data.keys())}")
                    
                    # Current veri kontrolü
                    current = weather_data.get('current', {})
                    if current:
                        _LOGGER.debug(f"Current data: temp={current.get('temperature_2m')}, humidity={current.get('relative_humidity_2m')}")
                    
                    # Daily veri kontrolü
                    daily = weather_data.get('daily', {})
                    if daily:
                        times = daily.get('time', [])
                        _LOGGER.debug(f"Daily forecast: {len(times)} days")
                        _LOGGER.debug(f"Daily forecast keys: {list(daily.keys())}")
                        if times:
                            _LOGGER.debug(f"Daily time range: {times[0]} to {times[-1]}")
                    
                    return weather_data
                else:
                    error_msg = data.get('error', 'Bilinmeyen hata')
                    _LOGGER.error(f"API hatası: {error_msg}")
                    if 'file' in data:
                        _LOGGER.error(f"Hata dosyası: {data.get('file')}, Satır: {data.get('line')}")
                    return None
            else:
                _LOGGER.error(f"HTTP hatası: {response.status_code}")
                try:
                    error_data = response.json()
                    if error_data.get('error'):
                        _LOGGER.error(f"API hatası: {error_data.get('error')}")
                except:
                    _LOGGER.error(f"Response: {response.text[:500]}")
                return None
                
        except Exception as e:
            _LOGGER.error(f"API bağlantı hatası: {e}")
            return None
