from flask import Flask, render_template, abort, request
import os
import pandas as pd
from datetime import date
import subprocess

app = Flask(__name__)

BASE_DIR = "data"
TODAY = date.today().isoformat()
TODAY_DIR = os.path.join(BASE_DIR, TODAY)

# ---------------- HELPERS ----------------

def list_dates():
    if not os.path.exists(BASE_DIR):
        return []
    return sorted(
        [d for d in os.listdir(BASE_DIR)
         if os.path.isdir(os.path.join(BASE_DIR, d))],
        reverse=True
    )

# ---------------- HOME ----------------

@app.route("/")
def home():
    summary = None
    final_file = os.path.join(TODAY_DIR, "final_dataset.csv")

    if os.path.exists(final_file):
        df = pd.read_csv(final_file)

        if not df.empty:
            summary = {
                "date": TODAY,
                "total": len(df),
                "top_topic": df["topic"].value_counts().idxmax()
                if "topic" in df.columns else "N/A"
            }

    return render_template("index.html", summary=summary)

# ---------------- RUN AGENT ----------------

@app.route("/run-agent")
def run_agent():
    subprocess.run(["python", "main.py"])
    return "<h2>Agent executed successfully</h2><a href='/'>Back</a>"

# ---------------- TODAY FILE VIEW ----------------

@app.route("/today/<kind>")
def today(kind):
    return show_csv(TODAY_DIR, kind)

# ---------------- HISTORY WITH SEARCH ----------------

@app.route("/history")
def history():
    dates = list_dates()
    search_date = request.args.get("search")
    filtered_dates = dates
    message = None

    if search_date:
        search_date = search_date.strip()

        if search_date in dates:
            filtered_dates = [search_date]
        else:
            if dates:
                message = f"Data stored between {dates[-1]} to {dates[0]}"
                filtered_dates = []
            else:
                message = "No data available."

    return render_template(
        "history.html",
        dates=filtered_dates,
        message=message,
        search_value=search_date if search_date else ""
    )

@app.route("/history/<day>/<kind>")
def history_view(day, kind):
    folder = os.path.join(BASE_DIR, day)
    if not os.path.exists(folder):
        abort(404)
    return show_csv(folder, kind)

# ---------------- SHOW CSV ----------------

def show_csv(folder, kind):
    file_map = {
        "raw": "raw_data.csv",
        "processed": "processed_data.csv",
        "final": "final_dataset.csv"
    }

    if kind not in file_map:
        abort(404)

    csv_path = os.path.join(folder, file_map[kind])

    if not os.path.exists(csv_path):
        return f"<h2>{kind.capitalize()} file not found</h2><a href='/history'>Back</a>"

    df = pd.read_csv(csv_path)

    if df.empty:
        return f"<h2>{kind.capitalize()} file is empty</h2><a href='/history'>Back</a>"

    table_html = df.to_html(classes="table table-striped", index=False)

    return render_template(
        "table.html",
        table=table_html,
        kind=kind
    )

# ---------------- START ----------------

if __name__ == "__main__":
    app.run(debug=True)