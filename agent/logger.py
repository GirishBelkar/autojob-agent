import csv
import os
from datetime import datetime

LOG_FILE = "data/job_log.csv"


def log_job(job, score, status):
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(["Date", "Title", "Company", "Score", "Status"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            job["title"],
            job["company"],
            score,
            status
        ])
