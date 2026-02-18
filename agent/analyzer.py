import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {API_KEY}"}


def analyze_job(job, profile):
    print("🤖 Analyzing job with AI...")

    prompt = f"""
Evaluate candidate match.

JOB:
{job['description']}

PROFILE:
{profile}

Return format:
Score: <0-100>
Explanation:
"""

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    result = response.json()

    try:
        text = result[0]["generated_text"]
    except:
        text = str(result)

    score_match = re.search(r"Score:\s*(\d+)", text)
    score = int(score_match.group(1)) if score_match else 50

    return {"score": score, "analysis": text}
