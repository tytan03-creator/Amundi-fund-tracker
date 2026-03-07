cat > scraper.py << 'ENDOFFILE'
import json
import re
import time
from datetime import datetime
from playwright.sync_api import sync_playwright

FUNDS = [
    {
        "id": "LU2420245917",
        "short": "S&P 500 ESG",
        "url": "https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420245917:SGD",
        "summary_url": "https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420245917:SGD"
    },
    {
        "id": "LU2420246139",
        "short": "MSCI World",
        "url": "https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420246139:SGD",
        "summary_url": "https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420246139:SGD"
    },
    {
        "id": "LU2420246055",
        "short": "MSCI EM",
        "url": "https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420246055:SGD",
        "summary_url": "https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420246055:SGD"
    },
    {
        "id": "LU2420246212",
        "short": "MSCI Europe",
        "url": "https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420246212:SGD",
        "summary_url": "https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420246212:SGD"
    }
]

def scrape_fund(page, fund):
    print("Scraping " + fund["short"] + "...")
    page.goto(fund["url"], wait_until="networkidle", timeout=60000)
    time.sleep(3)
    page.wait_for_selector("table", timeout=30000)

    rows = page.query_selector_all("table tbody tr")
    prices = []

    for row in rows:
        cols = row.query_selector_all("td")
        if len(cols) >= 2:
            date_text = cols[0].inner_text().strip()
            price_text = cols[1].inner_text().strip()
            price_clean = re.sub(r"[^\d.]", "", price_text)
            try:
                price_val = float(price_clean)
                prices.append({"date": date_text, "price": price_val})
            except ValueError:
                continue

    return prices

def calculate_changes(prices):
    result = []
    for i, entry in enumerate(prices):
        if i < len(prices) - 1:
            prev_price = prices[i + 1]["price"]
            curr_price = entry["price"]
            pct_change = ((curr_price - prev_price) / prev_price) * 100
        else:
            pct_change = None
        result.append({
            "date": entry["date"],
            "price": entry["price"],
            "pct_change": pct_change
        })
    return result

def find_jan2_price(prices):
    for entry in reversed(prices):
        if ("Jan 02" in entry["date"] or "Jan 2," in entry["date"]) and "2026" in entry["date"]:
            return entry["price"]
    if prices:
        return prices[-1]["price"]
    return None

def main():
    all_data = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for fund in FUNDS:
            try:
                raw_prices = scrape_fund(page, fund)
                if not raw_prices:
                    print("  No prices found for " + fund["short"])
                    continue

                priced = calculate_changes(raw_prices)[:5]
                jan2_price = find_jan2_price(raw_prices)
                latest_price = raw_prices[0]["price"] if raw_prices else None
                ytd_pct = None
                if jan2_price and latest_price:
                    ytd_pct = ((latest_price - jan2_price) / jan2_price) * 100

                all_data[fund["id"]] = {
                    "short": fund["short"],
                    "url": fund["summary_url"],
                    "historical_url": fund["url"],
                    "prices": priced,
                    "jan2_price": jan2_price,
                    "ytd_pct": ytd_pct
                }
                print("  Got " + str(len(priced)) + " days of data")

            except Exception as e:
                print("  Error scraping " + fund["short"] + ": " + str(e))

        browser.close()

    output = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "funds": all_data
    }

    with open("data.json", "w") as f:
        json.dump(output, f, indent=2)

    print("Done! Data saved to data.json")

if __name__ == "__main__":
    main()
ENDOFFILE
