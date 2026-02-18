import requests


def search_jobs(role, location):
    print("🌐 Fetching real jobs using Remotive API...\n")

    search_terms = [role, "Python", "Data", "Machine Learning", "AI"]

    jobs = []

    for term in search_terms:
        url = f"https://remotive.com/api/remote-jobs?search={term}"
        response = requests.get(url)
        data = response.json()

        for job in data.get("jobs", [])[:2]:
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "description": job["description"][:500]
            })

        if len(jobs) >= 6:
            break

    return jobs
