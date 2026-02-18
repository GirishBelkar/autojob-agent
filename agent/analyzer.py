import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}


def analyze_job(job, profile):
    print("🤖 Using FREE HuggingFace model to analyze job...")

    prompt = f"""
Analyze the job and candidate profile.

JOB DESCRIPTION:
{job['description']}

CANDIDATE PROFILE:
{profile}

Provide:
- Required skills
- Matching skills
- Missing skills
- Short evaluation
"""

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    result = response.json()

    try:
        text = result[0]["generated_text"]
    except Exception:
        text = str(result)

    return {
        "match_summary": text,
        "missing_skills": "Check analysis above."
    }
