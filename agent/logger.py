import csv
import os
from datetime import datetime

LOG_FILE = "data/job_log.csv"


def job_already_processed(job):
    """
    Check if this job already exists in the log file.
    Matching is based on Title + Company.
    Handles Windows CSV encoding safely.
    """

    if not os.path.isfile(LOG_FILE):
        return False  # No history yet

    with open(LOG_FILE, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        if len(rows) <= 1:
            return False  # No data yet

        header = [h.strip().lower() for h in rows[0]]

        try:
            title_index = header.index("title")
            company_index = header.index("company")
        except ValueError:
            return False  # Header mismatch, ignore safely

        for row in rows[1:]:
            if len(row) <= max(title_index, company_index):
                continue

            logged_title = row[title_index].strip().lower()
            logged_company = row[company_index].strip().lower()

            if (
                logged_title == job["title"].strip().lower()
                and logged_company == job["company"].strip().lower()
            ):
                return True

    return False


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
