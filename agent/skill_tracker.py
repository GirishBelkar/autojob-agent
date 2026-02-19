import os
import re
from collections import Counter

from agent.learning_planner import generate_daily_plan

OUTPUT_DIR = "outputs"


def extract_missing_skills():
    """
    Reads insight files and extracts real missing skills.
    Ignores placeholders like 'Not Identified'.
    """
    skill_counter = Counter()

    if not os.path.exists(OUTPUT_DIR):
        return skill_counter

    for file in os.listdir(OUTPUT_DIR):
        if not file.endswith(".txt"):
            continue

        path = os.path.join(OUTPUT_DIR, file)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.strip().lower() == "missing skills":
                # Next meaningful line contains the skills
                if i + 2 < len(lines):
                    skills_line = lines[i + 2].strip()

                    # 🚫 Ignore placeholders
                    if skills_line.lower() in ["not identified", "none", "n/a", ""]:
                        continue

                    # ✅ Split real skills
                    skills = [s.strip().lower() for s in skills_line.split(",")]

                    for skill in skills:
                        if len(skill) > 2:  # avoid single letters
                            skill_counter[skill] += 1

    return skill_counter


def collect_missing_skills(_=None):
    """
    Called by AutoJobAgent after job scan.
    Generates report + learning plan.
    """
    skills = extract_missing_skills()

    if not skills:
        print("📚 No skill gaps detected yet.")
        return

    print("\n📊 MARKET SKILL GAP REPORT")
    print("--------------------------")

    for skill, count in skills.most_common():
        print(f"{skill.title()} → mentioned {count} times")

    # Take top 5 demanded skills
    priority_skills = [skill for skill, _ in skills.most_common(5)]

    print("\n🎯 Priority Skills To Learn Next:")
    for skill in priority_skills:
        print(f"   - {skill.title()}")

    # Send to planner
    generate_daily_plan(priority_skills)


# (Optional — used by runner if called directly)
def generate_learning_report():
    collect_missing_skills()
