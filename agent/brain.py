from agent.job_search import search_jobs
from agent.job_search_extended import search_jobs_extended   # ✅ NEW SOURCE
from agent.analyzer import analyze_job
from agent.resume_builder import build_application
from agent.logger import log_job, job_already_processed
from agent.preferences import should_skip_based_on_preferences
from agent.notifier import send_job_alert
from agent.skill_tracker import collect_missing_skills        # ✅ we will use this


class AutoJobAgent:
    def __init__(self, profile):
        self.profile = profile
        self.missing_skills_accumulator = set()   # Track skills across jobs

    def run(self, role, location):
        print(f"\n🔍 Searching jobs for {role} in {location}...\n")

        # ✅ MULTI-SOURCE SEARCH
        jobs_primary = search_jobs(role, location)
        jobs_secondary = search_jobs_extended(role, location)

        jobs = jobs_primary + jobs_secondary

        if not jobs:
            print("❌ No jobs found.")
            return

        SHORTLIST_THRESHOLD = 60

        for job in jobs:
            print(f"📄 Found Job: {job['title']} at {job['company']}")

            # 🧠 MEMORY CHECK — Skip jobs already processed before
            if job_already_processed(job):
                print("⏩ Already processed. Skipping.\n")
                continue

            # 🎯 PREFERENCE FILTER
            if should_skip_based_on_preferences(job, self.profile):
                print("🧠 Skipped by learned preferences.\n")
                continue

            # 🤖 AI ANALYSIS
            insights = analyze_job(job, self.profile)
            score = insights.get("score", 50)
            reason = insights.get("summary", "Matched based on profile analysis.")
            missing_skills = insights.get("missing_skills", [])

            # Collect missing skills for learning plan
            self.missing_skills_accumulator.update(missing_skills)

            print(f"📊 Match Score: {score}")

            status = "Shortlisted" if score >= SHORTLIST_THRESHOLD else "Skipped"

            if status == "Shortlisted":
                print("✅ Shortlisted — Sending Email Alert\n")

                send_job_alert(
                    to_email="YOUR_EMAIL@gmail.com",  # change this
                    job_title=job["title"],
                    company=job["company"],
                    link=job.get("url", "No link provided"),
                    score=score,
                    reason=reason
                )
            else:
                print("❌ Skipped\n")

            # Log every evaluated job
            log_job(job, score, status)

            # Generate insight file
            build_application(job, insights, self.profile)

        print("\n🎯 Shortlisting completed.")

        # ✅ AFTER ALL JOBS → CREATE LEARNING PLAN
        if self.missing_skills_accumulator:
            print("\n📚 Creating daily learning plan...\n")
            collect_missing_skills(list(self.missing_skills_accumulator))
        else:
            print("\n📘 No new skills identified today.")
