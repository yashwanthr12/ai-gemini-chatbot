import re
from chatbot.tools import tool_bitcoin_price, tool_weather

def extract_city(text: str) -> str | None:
    """
    Extract everything after the word 'weather' (optionally 'in').
    Examples:
      - "weather in Bangalore"
      - "Weather in Bangalore, Rajarajesshwari nagar"
      - "weather Bangalore"
    """
    t = text.strip()

    # Remove a trailing question mark etc.
    t = re.sub(r"[?!.]+$", "", t)

    m = re.search(r"\bweather\b(?:\s+in)?\s+(.*)$", t, re.IGNORECASE)
    if not m:
        return None

    city = m.group(1).strip()
    # If user wrote only "weather" with nothing else
    if not city:
        return None
    return city

def route(user_input: str) -> dict:
    text = user_input.lower()

    if "bitcoin" in text or ("price" in text and ("btc" in text or "bitcoin" in text or "crypto" in text)):
        tool_text = tool_bitcoin_price()
        return {"route": "crypto", "tool_text": tool_text}

    if "weather" in text:
        city = extract_city(user_input) or "London"
        tool_text = tool_weather(city)
        return {"route": "weather", "tool_text": tool_text}

    return {"route": "gemini", "tool_text": ""}