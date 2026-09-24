import requests
import csv
import os
from datetime import datetime

API_KEY = "3a1ad755f19047aca2dc8cb8aa840163"   # put your real key here

DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "raw_data.csv")

os.makedirs(DATA_DIR, exist_ok=True)

url = "https://newsapi.org/v2/top-headlines"
params = {
    "country": "us",
    "pageSize": 20,
    "apiKey": API_KEY
}

response = requests.get(url, params=params)

if response.status_code != 200:
    print("Failed to fetch news")
    exit()

articles = response.json().get("articles", [])

if not articles:
    print("No articles returned from API")
    exit()

with open(RAW_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "topic", "timestamp"])
    writer.writeheader()

    for article in articles:
        title = article.get("title")
        desc = article.get("description")
        content = f"{title} {desc}" if desc else title

        if content:
            writer.writerow({
                "text": content,
                "topic": "general",
                "timestamp": datetime.utcnow().isoformat()
            })

print(f"AGENT INGESTED {len(articles)} ITEMS")