import os
import requests
from utils.logger import setup_logger

logger = setup_logger("api_clients")

class CryptoClient:
    """
    Uses CoinGecko public API (no API key required).
    """
    BASE_URL = "https://api.coingecko.com/api/v3"

    def get_bitcoin_price_usd(self) -> float:
        url = f"{self.BASE_URL}/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd"}
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        return float(data["bitcoin"]["usd"])


class WeatherClient:
    """
    Uses OpenWeatherMap API (API key required).
    """
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()
        if not self.api_key:
            logger.warning("OPENWEATHER_API_KEY is missing. Weather tool will fail.")

    def get_weather(self, city: str, units: str = "metric") -> dict:
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is not set in .env")

        params = {"q": city, "appid": self.api_key, "units": units}
        r = requests.get(self.BASE_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        return {
            "city": data.get("name", city),
            "country": data.get("sys", {}).get("country", ""),
            "temp": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "description": (data.get("weather") or [{}])[0].get("description"),
            "wind_speed": data.get("wind", {}).get("speed"),
        }