import requests
from app.core.config import settings

BASE_URL = "https://api.polygon.io/v1/open-close"

def get_daily_stock(symbol: str, date: str):
    """
    Busca os dados de open, high, low, close para um stock num dia específico.
    date precisa estar no formato YYYY-MM-DD.
    """
    url = f"{BASE_URL}/{symbol.upper()}/{date}"
    headers = {
        "Authorization": f"Bearer {settings.POLYGON_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Polygon API error: {response.status_code} - {response.text}")

    data = response.json()
    return {
        "status": data.get("status", "OK"),
        "open": data.get("open"),
        "high": data.get("high"),
        "low": data.get("low"),
        "close": data.get("close"),
    }
