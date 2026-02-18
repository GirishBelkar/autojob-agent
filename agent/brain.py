from agent.job_search import search_jobs
from agent.analyzer import analyze_job
from agent.resume_builder import build_application


class AutoJobAgent:
    def __init__(self, profile):
        self.profile = profile

    def run(self, role, location):
        print(f"\n🔍 Searching jobs for {role} in {location}...\n")

        jobs = search_jobs(role, location)

        if not jobs:
            print("❌ No jobs found.")
            return

        for job in jobs:
            print(f"📄 Found Job: {job['title']} at {job['company']}")

            insights = analyze_job(job, self.profile)

            build_application(job, insights, self.profile)

        print("\n✅ All applications generated inside /outputs folder.")
