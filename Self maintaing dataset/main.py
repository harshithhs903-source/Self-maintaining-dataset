import os
import pandas as pd
from datetime import date

# ---------------- SETUP ----------------

BASE_DIR = "data"
TODAY = date.today().isoformat()
today_folder = os.path.join(BASE_DIR, TODAY)

os.makedirs(today_folder, exist_ok=True)

raw_path = os.path.join(today_folder, "raw_data.csv")
processed_path = os.path.join(today_folder, "processed_data.csv")
final_path = os.path.join(today_folder, "final_dataset.csv")

# ---------------- RAW DATA ----------------

sample_articles = [
    "Government announces new election reforms!!!",
    "Stock market sees major growth in tech sector.",
    "AI startup launches NEW software platform.",
    "Football tournament final ends dramatically!!",
    "New medical research shows promising results.",
    "Hollywood movie breaks box office records!!",
    "Scientists discover new space phenomenon."
]

raw_df = pd.DataFrame({"text": sample_articles})
raw_df.to_csv(raw_path, index=False)

print("Raw data created.")

# ---------------- PROCESSING ----------------

processed_df = raw_df.copy()

# Real cleaning
processed_df["clean_text"] = (
    processed_df["text"]
    .str.lower()
    .str.replace(r"[^\w\s]", "", regex=True)
)

processed_df[["clean_text"]].to_csv(processed_path, index=False)

print("Processed data created.")

# ---------------- TOPIC CLASSIFICATION ----------------

def categorize_topic(text):
    if "election" in text or "government" in text:
        return "Politics"
    elif "stock" in text or "market" in text:
        return "Business"
    elif "ai" in text or "software" in text:
        return "Tech"
    elif "football" in text:
        return "Sports"
    elif "movie" in text:
        return "Entertainment"
    elif "medical" in text:
        return "Health"
    elif "science" in text or "space" in text:
        return "Science"
    else:
        return "World"

processed_df["topic"] = processed_df["clean_text"].apply(categorize_topic)

final_df = processed_df[["clean_text", "topic"]]
final_df.columns = ["text", "topic"]
final_df.to_csv(final_path, index=False)

print("Final dataset created.")
print("Agent completed successfully.")