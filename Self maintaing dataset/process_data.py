import csv
import os

DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "raw_data.csv")
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_data.csv")

if not os.path.exists(RAW_FILE):
    print("No raw data found. Skipping processing.")
    exit()

with open(RAW_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

cleaned_rows = []

for r in rows:
    text = r["text"].strip().lower()
    topic = r["topic"]

    if text:
        cleaned_rows.append({
            "clean_text": text,
            "topic": topic
        })

with open(PROCESSED_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["clean_text", "topic"])
    writer.writeheader()
    writer.writerows(cleaned_rows)

print(f"PROCESSED {len(cleaned_rows)} ROWS")