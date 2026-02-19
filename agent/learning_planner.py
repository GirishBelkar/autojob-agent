import datetime
import os


def generate_daily_plan(missing_skills):
    """
    Creates a daily study plan based on detected missing skills.
    """

    today = datetime.date.today()

    if not missing_skills:
        print("📘 No new skills to learn today.")
        return

    # Create folder if not exists
    os.makedirs("learning", exist_ok=True)

    filename = f"learning/plan_{today}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📅 Learning Plan for {today}\n")
        f.write("=" * 40 + "\n\n")

        for skill in missing_skills:
            f.write(f"🔹 Focus Skill: {skill.title()}\n")

            # Basic roadmap logic
            if "pandas" in skill.lower():
                f.write("   → Practice DataFrames (30 min)\n")
                f.write("   → Load CSV + Clean Data\n\n")

            elif "sql" in skill.lower():
                f.write("   → Write SELECT queries (30 min)\n")
                f.write("   → Practice JOIN + GROUP BY\n\n")

            elif "python" in skill.lower():
                f.write("   → Solve 5 beginner problems\n\n")

            elif "excel" in skill.lower():
                f.write("   → Practice formulas + pivot tables\n\n")

            else:
                f.write("   → Watch tutorial + take notes (45 min)\n\n")

    print(f"📚 Daily learning plan created → {filename}")
