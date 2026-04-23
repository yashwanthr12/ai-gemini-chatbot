from utils.api_clients import CryptoClient, WeatherClient

crypto_client = CryptoClient()
weather_client = WeatherClient()

def tool_bitcoin_price() -> str:
    price = crypto_client.get_bitcoin_price_usd()
    return f"Bitcoin (BTC) current price: ${price:,.2f} USD"

def tool_weather(city: str) -> str:
    try:
        w = weather_client.get_weather(city)
        return (
            f"Weather for {w['city']}, {w['country']}:\n"
            f"- Description: {w['description']}\n"
            f"- Temperature: {w['temp']}°C (feels like {w['feels_like']}°C)\n"
            f"- Humidity: {w['humidity']}%\n"
            f"- Wind speed: {w['wind_speed']} m/s"
        )
    except Exception as e:
        # Never crash the whole chatbot because a tool failed
        return (
            f"Weather tool failed for city='{city}'.\n"
            f"Reason: {type(e).__name__}: {e}\n"
            f"Fix: Check OPENWEATHER_API_KEY in .env (valid/active), then restart the app."
        )