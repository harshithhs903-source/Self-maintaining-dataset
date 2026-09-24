import os
import pandas as pd
import re

BASE_DIR = "data"

# ---------------- CLEANING ----------------

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text.strip()

# ---------------- TOPIC ----------------

def categorize_topic(text):
    text = str(text).lower()

    if any(word in text for word in ["election","president","government","senate",
                                     "minister","congress","vote","political"]):
        return "Politics"

    elif any(word in text for word in ["stock","market","company","business",
                                       "economy","trade","finance","bank"]):
        return "Business"

    elif any(word in text for word in ["technology","ai","software","tech",
                                       "startup","robot","cyber","app"]):
        return "Tech"

    elif any(word in text for word in ["match","tournament","football",
                                       "cricket","nba","goal","sports"]):
        return "Sports"

    elif any(word in text for word in ["movie","music","celebrity",
                                       "show","hollywood","film"]):
        return "Entertainment"

    elif any(word in text for word in ["health","disease","doctor",
                                       "medical","virus","hospital"]):
        return "Health"

    elif any(word in text for word in ["science","research",
                                       "study","scientist","space"]):
        return "Science"

    else:
        return "World"


# ---------------- LOOP ALL DATE FOLDERS ----------------

for folder in os.listdir(BASE_DIR):
    full_path = os.path.join(BASE_DIR, folder)

    if not os.path.isdir(full_path):
        continue

    raw_path = os.path.join(full_path, "raw_data.csv")
    processed_path = os.path.join(full_path, "processed_data.csv")
    final_path = os.path.join(full_path, "final_dataset.csv")

    if not os.path.exists(raw_path):
        continue

    df = pd.read_csv(raw_path)

    if "text" not in df.columns:
        continue

    # Clean + recalc topic
    df["clean_text"] = df["text"].apply(clean_text)
    df["topic"] = df["clean_text"].apply(categorize_topic)

    # Overwrite processed
    processed_df = df[["clean_text", "topic"]]
    processed_df.to_csv(processed_path, index=False)

    # Overwrite final
    final_df = processed_df.copy()
    final_df.columns = ["text","topic"]
    final_df.to_csv(final_path, index=False)

    print(f"{folder} fixed ✔")

print("All previous days updated successfully.")