import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def analyze_job(job, profile):
    print("🤖 Using AI to analyze job...")

    prompt = f"""
You are a career assistant AI.

JOB DESCRIPTION:
{job['description']}

CANDIDATE PROFILE:
{profile}

Do the following:
1. Extract key required skills.
2. Compare with candidate profile.
3. Identify missing skills.
4. Write a short match evaluation.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    result = response.choices[0].message.content

    return {
        "match_summary": result,
        "missing_skills": "See AI analysis above."
    }
