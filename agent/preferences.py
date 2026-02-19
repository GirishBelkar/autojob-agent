"""
Preference Engine
Simulates behavioral learning from past outcomes.
"""

DISCOURAGED_KEYWORDS = [
    "senior",
    "lead",
    "manager",
    "principal",
    "staff",
    "architect",
    "director"
]


def should_skip_based_on_preferences(job, profile):
    """
    Decide whether to skip a job before LLM analysis.
    This mimics learned behavior for fresher-level candidates.
    """

    title = job["title"].lower()

    # If candidate is fresher, avoid senior-heavy roles
    if profile and "fresher" in profile.lower():
        for word in DISCOURAGED_KEYWORDS:
            if word in title:
                return True

    return False
