import requests


def search_jobs(role, location):
    print("🌐 Fetching real jobs using Remotive API...\n")

    # Agent expands search automatically
    search_terms = [
        role,
        "Python",
        "Data",
        "Machine Learning",
        "AI",
        "Backend"
    ]

    jobs = []

    for term in search_terms:
        url = f"https://remotive.com/api/remote-jobs?search={term}"

        try:
            response = requests.get(url)
            data = response.json()
        except Exception:
            continue

        for job in data.get("jobs", [])[:2]:  # take few per term
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "description": job["description"][:500]
            })

        if len(jobs) >= 6:
            break

    return jobs
