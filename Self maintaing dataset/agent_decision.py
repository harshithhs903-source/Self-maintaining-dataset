import csv
import os
from transformers import pipeline

DATA_DIR = "data"
PROCESSED_FILE = os.path.join(DATA_DIR, "processed_data.csv")
FINAL_FILE = os.path.join(DATA_DIR, "final_dataset.csv")

print("Loading AI sentiment model...")
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

if not os.path.exists(PROCESSED_FILE):
    print("No processed data found.")
    exit()

with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

accepted = []
rejected = []

for r in rows:
    text = r["clean_text"]

    # Basic quality rule
    if len(text.split()) < 5:
        rejected.append([text, r["topic"], "REJECTED", "Too short", "-", "-"])
        continue

    # AI sentiment analysis
    result = classifier(text[:512])[0]
    sentiment = result["label"]
    confidence = round(result["score"], 4)

    # Decision logic
    if confidence > 0.75:
        decision = "ACCEPTED"
        accepted.append([text, r["topic"], decision, sentiment, confidence, "AI_CONFIDENT"])
    else:
        rejected.append([text, r["topic"], "REJECTED", sentiment, confidence, "LOW_CONFIDENCE"])

# Save final dataset
with open(FINAL_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["text", "topic", "decision", "sentiment", "confidence", "reason"])
    
    for row in accepted:
        writer.writerow(row)
    for row in rejected:
        writer.writerow(row)

print(f"\nAGENT DECISION COMPLETE")
print(f"Accepted: {len(accepted)}")
print(f"Rejected: {len(rejected)}")