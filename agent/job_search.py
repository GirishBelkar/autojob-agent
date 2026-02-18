import requests


def search_jobs(role, location):
    print("🌐 Fetching real jobs using Remotive API...\n")

    url = f"https://remotive.com/api/remote-jobs?search={role}"

    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print("API error:", e)
        return []

    jobs = []

    for job in data.get("jobs", [])[:5]:
        jobs.append({
            "title": job["title"],
            "company": job["company_name"],
            "description": job["description"][:500]  # limit text size
        })

    return jobs
