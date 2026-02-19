from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, User, Profile
from .auth import hash_password, verify_password

import subprocess

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SIGNUP ----------------
@app.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup")
def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = User(name=name, email=email, password=hash_password(password))
    db.add(user)
    db.commit()

    return RedirectResponse("/login", status_code=303)


# ---------------- LOGIN ----------------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        return RedirectResponse("/login", status_code=303)

    response = RedirectResponse("/onboarding", status_code=303)
    response.set_cookie("user_id", str(user.id))
    return response


# ---------------- ONBOARDING ----------------
@app.get("/onboarding")
def onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})


@app.post("/onboarding")
def save_profile(
    request: Request,
    target_role: str = Form(...),
    location: str = Form(...),
    experience_level: str = Form(...),
    skills: str = Form(...),
    career_goal: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")

    profile = Profile(
        user_id=user_id,
        target_role=target_role,
        location=location,
        experience_level=experience_level,
        skills=skills,
        career_goal=career_goal
    )

    db.add(profile)
    db.commit()

    return RedirectResponse("/", status_code=303)


# ---------------- DASHBOARD ----------------
@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Run agent from UI
@app.post("/run-agent")
def run_agent():
    subprocess.Popen(["python", "runner.py"])
    return {"status": "started"}
