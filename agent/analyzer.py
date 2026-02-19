import os
import requests
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
headers = {"Authorization": f"Bearer {API_KEY}"}


# -----------------------------
# CLEAN SKILL TEXT FROM LLM
# -----------------------------
def _clean_skill_list(raw_text):
    if not raw_text:
        return []

    raw_text = raw_text.strip()

    if raw_text.lower() in ["not identified", "none", "n/a"]:
        return []

    skills = [s.strip().lower() for s in raw_text.split(",")]

    cleaned = []
    for skill in skills:
        if len(skill) < 2:
            continue
        if skill in ["and", "or"]:
            continue
        cleaned.append(skill)

    return list(set(cleaned))


# -----------------------------
# RULE-BASED EXTRACTION (RELIABLE)
# -----------------------------
def extract_skills_from_description(text):
    text = text.lower()

    SKILL_LIBRARY = [
        "python", "sql", "pandas", "numpy", "excel",
        "power bi", "tableau", "statistics",
        "machine learning", "data analysis",
        "data visualization", "etl", "dashboard",
        "aws", "azure"
    ]

    detected = []

    for skill in SKILL_LIBRARY:
        if skill in text:
            detected.append(skill)

    return detected


# -----------------------------
# SIMPLE MATCH SCORING ENGINE
# -----------------------------
def calculate_score(profile, detected_skills):
    profile_text = profile.lower()

    user_skills = []
    for skill in detected_skills:
        if skill in profile_text:
            user_skills.append(skill)

    if not detected_skills:
        return 40  # unknown job

    match_ratio = len(user_skills) / len(detected_skills)

    score = int(match_ratio * 100)

    # Clamp range
    score = max(30, min(score, 90))

    return score


# -----------------------------
# MAIN ANALYSIS FUNCTION
# -----------------------------
def analyze_job(job, profile):
    print("🤖 Analyzing job with AI...")

    description = job.get("description", "")

    prompt = f"""
Evaluate this candidate vs job.

JOB:
{description}

CANDIDATE:
{profile}

Return:
Strengths:
Missing Skills:
Recommendation:
"""

    # ---- Call LLM (optional reasoning) ----
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=25)
        result = response.json()
        text = result[0]["generated_text"]
    except Exception:
        text = "LLM unavailable — using deterministic analysis."

    # ---- Extract from LLM if possible ----
    strengths_match = re.search(r"Strengths:\s*(.*)", text)
    missing_match = re.search(r"Missing Skills:\s*(.*)", text)
    recommendation_match = re.search(r"Recommendation:\s*(.*)", text)

    strengths_llm = _clean_skill_list(strengths_match.group(1)) if strengths_match else []
    missing_llm = _clean_skill_list(missing_match.group(1)) if missing_match else []

    # ---- Always run deterministic extraction ----
    detected_skills = extract_skills_from_description(description)

    # Combine both
    missing_skills = list(set(detected_skills + missing_llm))

    # ---- Calculate realistic score ----
    score = calculate_score(profile, detected_skills)

    recommendation = (
        recommendation_match.group(1).strip()
        if recommendation_match
        else "Improve missing tools to better match this role."
    )

    return {
        "score": score,
        "strengths": strengths_llm,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "summary": recommendation,
        "analysis": text
    }
