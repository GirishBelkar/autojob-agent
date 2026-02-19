import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_job_alert(to_email, job_title, company, link, score, reason):
    sender_email = "YOUR_EMAIL@gmail.com"
    app_password = "YOUR_APP_PASSWORD"   # Not your real password!

    subject = f"🔥 Job Match Found: {job_title} at {company}"

    body = f"""
Good news Girish!

Your AutoJob Agent found a strong match.

📌 Role: {job_title}
🏢 Company: {company}
📊 Match Score: {score}

Why this matches you:
{reason}

Apply here:
{link}

— Your AI Job Agent 🤖
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()
        print("📧 Email alert sent!")
    except Exception as e:
        print("❌ Email failed:", e)
