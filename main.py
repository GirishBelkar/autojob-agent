from agent.brain import AutoJobAgent


profile = """
Name: Girish Belkar
Skills: Python, FastAPI (learning), Data Analysis (learning), AI Enthusiast
Goal: Entry-level AI / Data role
"""


agent = AutoJobAgent(profile)

agent.run(role="Data Analyst", location="Mumbai")
