import requests


def search_jobs_extended(role, location):
    print("🌐 Fetching jobs from public search...")

    query = f"{role} in {location}"
    url = "https://remotive.com/api/remote-jobs"

    jobs_collected = []

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        for job in data.get("jobs", []):
            jobs_collected.append({
                "title": job["title"],
                "company": job["company_name"],
                "url": job["url"],
                "description": job["description"]
            })

    except Exception as e:
        print("❌ Extended search failed:", e)

    return jobs_collected
