import os
import asyncio
from datetime import datetime, timezone
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

class AlertRequest(BaseModel):
    email: EmailStr
    pass_time_utc: str
    pass_info: str

async def send_delayed_email(email: str, pass_time_utc: str, pass_info: str):
    try:
        pass_dt = datetime.strptime(pass_time_utc, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        target_time = pass_dt.timestamp() - 1800  # 30 minutes before pass
        now = datetime.now(timezone.utc).timestamp()
        delay = target_time - now

        if delay > 0:
            print(f"Timer started: Waiting {round(delay / 60, 1)} minutes to email {email}.")
            await asyncio.sleep(delay)
        
        if not SMTP_USERNAME or not SMTP_PASSWORD:
            print("Worker missing SMTP credentials.")
            return

        msg = MIMEMultipart()
        msg['From'] = f"Horizon Event Tracker <{SMTP_USERNAME}>"
        msg['To'] = email
        msg['Subject'] = "ISS Pass Approaching in 30 Minutes!"

        body = f"""
        OBSERVATION HEADS-UP
        
        {pass_info}
        Get ready! The ISS will be passing over your location in approximately 30 minutes.
        """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Successfully sent alert email to {email}")
            
    except Exception as e:
        print(f"Failed to execute scheduled email: {e}")

@app.post("/api/schedule-alert")
async def schedule_alert(data: AlertRequest, background_tasks: BackgroundTasks):
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        raise HTTPException(status_code=500, detail="SMTP credentials not configured on worker.")
    
    background_tasks.add_task(send_delayed_email, data.email, data.pass_time_utc, data.pass_info)
    return {"status": "success", "message": "Alert successfully queued on remote worker."}