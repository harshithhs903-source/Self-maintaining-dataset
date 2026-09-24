import os
import subprocess
from datetime import date

BASE_DIR = "data"
TODAY = date.today().isoformat()
TODAY_DIR = os.path.join(BASE_DIR, TODAY)

os.makedirs(TODAY_DIR, exist_ok=True)

print(f"Running full pipeline for {TODAY}")

# 1. Fetch news
os.system("python fetch_news.py")

# 2. Process data
os.system("python process_data.py")

# 3. Agent decision
os.system("python dataset_agent.py")

# 4. Move today files into today's folder
for filename in ["raw_data.csv", "processed_data.csv", "final_dataset.csv"]:
    src = os.path.join(BASE_DIR, filename)
    dst = os.path.join(TODAY_DIR, filename)
    if os.path.exists(src):
        os.replace(src, dst)

print("Today's data saved successfully.")