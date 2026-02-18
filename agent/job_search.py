import requests
from bs4 import BeautifulSoup


def search_jobs(role, location):
    print("🌐 Fetching real jobs from the web...\n")

    query = f"{role} {location}".replace(" ", "%20")
    url = f"https://www.indeed.com/jobs?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    jobs = []

    for card in soup.select(".job_seen_beacon")[:5]:
        title = card.select_one("h2")
        company = card.select_one(".companyName")
        summary = card.select_one(".job-snippet")

        if title and company and summary:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip(),
                "description": summary.text.strip()
            })

    if not jobs:
        print("⚠ Could not scrape jobs (site blocking). Using fallback data.")
        return []

    return jobs
