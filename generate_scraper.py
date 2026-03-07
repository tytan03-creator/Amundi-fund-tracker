code = [
    "import json",
    "import re",
    "import time",
    "from datetime import datetime",
    "from playwright.sync_api import sync_playwright",
    "",
    "FUNDS = [",
    "    {",
    "        " + repr("id") + ": " + repr("LU2420245917") + ",",
    "        " + repr("short") + ": " + repr("S&P 500 ESG") + ",",
    "        " + repr("url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420245917:SGD") + ",",
    "        " + repr("summary_url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420245917:SGD"),
    "    },",
    "    {",
    "        " + repr("id") + ": " + repr("LU2420246139") + ",",
    "        " + repr("short") + ": " + repr("MSCI World") + ",",
    "        " + repr("url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420246139:SGD") + ",",
    "        " + repr("summary_url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420246139:SGD"),
    "    },",
    "    {",
    "        " + repr("id") + ": " + repr("LU2420246055") + ",",
    "        " + repr("short") + ": " + repr("MSCI EM") + ",",
    "        " + repr("url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420246055:SGD") + ",",
    "        " + repr("summary_url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420246055:SGD"),
    "    },",
    "    {",
    "        " + repr("id") + ": " + repr("LU2420246212") + ",",
    "        " + repr("short") + ": " + repr("MSCI Europe") + ",",
    "        " + repr("url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/historical?s=LU2420246212:SGD") + ",",
    "        " + repr("summary_url") + ": " + repr("https://markets.ft.com/data/funds/tearsheet/summary?s=LU2420246212:SGD"),
    "    }",
    "]",
]

with open("scraper.py", "w", encoding="utf-8") as f:
    f.write("\n".join(code))

print("scraper.py written successfully")
