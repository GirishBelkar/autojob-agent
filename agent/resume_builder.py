import os
import re


def safe_filename(text):
    return re.sub(r'[<>:"/\\|?*]', '', text)


def build_application(job, insights, profile):
    os.makedirs("outputs", exist_ok=True)

    company = safe_filename(job['company'])
    title = safe_filename(job['title']).replace(" ", "_")

    filename = f"outputs/{company}_{title}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{insights['match_summary']}")

    print(f"✅ Application file created → {filename}")
