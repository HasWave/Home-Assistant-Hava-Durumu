"""Constants for HasWave Hava Durumu integration."""

DOMAIN = "haswave_hava_durumu"
DEFAULT_API_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_UPDATE_INTERVAL = 3600
DEFAULT_FORECAST_DAYS = 7

# WMO Weather Code mapping
WMO_TO_HA_CONDITION = {
    0: 'clear-day',
    1: 'partlycloudy',
    2: 'partlycloudy',
    3: 'cloudy',
    45: 'fog',
    48: 'fog',
    51: 'rainy',
    53: 'rainy',
    55: 'rainy',
    56: 'rainy',
    57: 'rainy',
    61: 'rainy',
    63: 'rainy',
    65: 'rainy',
    66: 'rainy',
    67: 'rainy',
    71: 'snowy',
    73: 'snowy',
    75: 'snowy',
    77: 'snowy',
    80: 'rainy',
    81: 'rainy',
    82: 'pouring',
    85: 'snowy',
    86: 'snowy',
    95: 'lightning',
    96: 'lightning-rainy',
    99: 'lightning-rainy',
}

