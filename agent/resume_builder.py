import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def build_application(job, insights, profile):
    """
    Creates an insight file for each analyzed job.
    """

    filename = f"{job['company']}_{job['title']}.txt"
    filename = filename.replace("/", "_").replace(" ", "_")

    path = os.path.join(OUTPUT_DIR, filename)

    summary = insights.get("summary", "No summary available.")
    score = insights.get("score", 50)

    # 🔴 IMPORTANT: ensure missing skills exist
    missing_skills = insights.get("missing_skills", [])

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Job: {job['title']} at {job['company']}\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"Match Score: {score}\n\n")

        f.write("Analysis Summary\n")
        f.write("----------------\n")
        f.write(summary + "\n\n")

        # ✅ THIS SECTION IS WHAT SKILL TRACKER NEEDS
        f.write("Missing Skills\n")
        f.write("--------------\n")

        if missing_skills:
            f.write(", ".join(missing_skills))
        else:
            f.write("Not Identified")

        f.write("\n")

    print(f"✅ Application insight file created → {path}")
