import os
import re


def safe_filename(text):
    # Remove invalid Windows filename characters
    return re.sub(r'[<>:"/\\|?*]', '', text)


def build_application(job, insights, profile):
    os.makedirs("outputs", exist_ok=True)

    company = safe_filename(job['company'])
    title = safe_filename(job['title']).replace(" ", "_")

    filename = f"outputs/{company}_{title}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Applying to: {job['title']} at {job['company']}\n")
        f.write("=" * 50 + "\n\n")

        f.write("CANDIDATE PROFILE:\n")
        f.write(profile + "\n\n")

        f.write("JOB MATCH ANALYSIS:\n")
        f.write(insights["match_summary"] + "\n\n")

        f.write("NOTE:\n")
        f.write(insights["missing_skills"])

    print(f"✅ Application file created → {filename}\n")
