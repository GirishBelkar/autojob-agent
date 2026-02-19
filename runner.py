import time
import schedule
import yaml

from agent.brain import AutoJobAgent
from agent.skill_tracker import generate_learning_report


def run_agent():
    print("\n🚀 Starting scheduled job scan...\n")

    # Load profile
    with open("config/user_profile.yaml", "r", encoding="utf-8") as file:
        profile_data = yaml.safe_load(file)

    # Convert profile into text for the LLM
    profile_text = (
        f"Name: {profile_data['name']}\n"
        f"Skills: {', '.join(profile_data['skills'])}\n"
        f"Experience Level: {profile_data['experience_level']}\n"
        f"Career Goal: {profile_data['career_goal']}"
    )

    # Run the main agent
    agent = AutoJobAgent(profile_text)
    agent.run(
        role=profile_data["target_role"],
        location=profile_data["location"]
    )

    # After scan, analyze missing skills
    print("\n🧠 Generating skill gap report...\n")
    generate_learning_report()

    print("\n😴 Job scan complete. Waiting for next run...\n")


# Schedule: run every day at 09:00 AM
schedule.every().day.at("09:00").do(run_agent)

print("⏰ AutoJob Agent Scheduler Started...")

# Run once immediately when script starts
run_agent()

# Keep scheduler alive
while True:
    schedule.run_pending()
    time.sleep(30)
