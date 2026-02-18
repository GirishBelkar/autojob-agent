from agent.job_search import search_jobs
from agent.analyzer import analyze_job
from agent.resume_builder import build_application
from agent.logger import log_job


class AutoJobAgent:
    def __init__(self, profile):
        self.profile = profile

    def run(self, role, location):
        print(f"\n🔍 Searching jobs for {role} in {location}...\n")

        jobs = search_jobs(role, location)

        if not jobs:
            print("❌ No jobs found.")
            return

        SHORTLIST_THRESHOLD = 60

        for job in jobs:
            print(f"📄 Found Job: {job['title']} at {job['company']}")

            insights = analyze_job(job, self.profile)
            score = insights.get("score", 50)

            print(f"📊 Match Score: {score}")

            if score >= SHORTLIST_THRESHOLD:
                print("✅ Shortlisted\n")
                log_job(job, score, "Shortlisted")

                build_application(
                    job,
                    {"match_summary": insights["analysis"], "missing_skills": ""},
                    self.profile
                )
            else:
                print("❌ Skipped\n")
                log_job(job, score, "Skipped")

        print("\n🎯 Shortlisting completed.")
