import yaml
from agent.brain import AutoJobAgent


def load_profile():
    with open("config/user_profile.yaml", "r") as file:
        return yaml.safe_load(file)


profile_data = load_profile()

profile_text = f"""
Name: {profile_data['name']}
Skills: {', '.join(profile_data['skills'])}
Experience Level: {profile_data['experience_level']}
Career Goal: {profile_data['career_goal']}
"""

agent = AutoJobAgent(profile_text)

agent.run(
    role=profile_data["target_role"],
    location=profile_data["location"]
)
