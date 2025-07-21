import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.marketwatch.com/investing/stock"

def get_marketwatch_data(symbol: str):
    url = f"{BASE_URL}/{symbol.lower()}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"MarketWatch error: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # --- COMPANY NAME ---
    name_tag = soup.find("h1", class_="company__name")
    company_name = name_tag.text.strip() if name_tag else symbol.upper()

    # --- PERFORMANCE DATA ---
    performance_data = {}
    perf_section = soup.find("div", class_="element element--table performance")
    if perf_section:
        rows = perf_section.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                label = cols[0].text.strip().lower()
                value = cols[1].text.strip()

                if "5 day" in label:
                    performance_data["five_days"] = value
                elif "1 month" in label:
                    performance_data["one_month"] = value
                elif "3 month" in label:
                    performance_data["three_months"] = value
                elif "ytd" in label:
                    performance_data["year_to_date"] = value
                elif "1 year" in label:
                    performance_data["one_year"] = value

    # --- COMPETITORS DATA ---
    competitors = []
    comp_section = soup.find("div", class_="element element--table overflow--table Competitors")
    if comp_section:
        rows = comp_section.find_all("tr")[1:]  # pula cabeçalho
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name_tag = cols[0].find("a", class_="link")
                name = name_tag.text.strip() if name_tag else ""

                # Pega variação em porcentagem (se existir)
                chg_tag = cols[1].find("bg-quote")
                chg_percent = chg_tag.text.strip() if chg_tag else cols[1].text.strip()

                market_cap = cols[2].text.strip()

                # Ignorar índices/commodities genéricos
                if any(x in name.lower() for x in ["s&p", "nasdaq", "vix", "gold", "oil"]):
                    continue

                competitors.append({
                    "name": name,
                    "chg_percent": chg_percent,
                    "market_cap": market_cap
                })

    return {
        "company_name": company_name,
        "performance_data": performance_data,
        "competitors": competitors,
    }
