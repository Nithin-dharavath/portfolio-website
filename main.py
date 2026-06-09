import logging
import re
from pathlib import Path

from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from middleware.rate_limit import contact_rate_limiter

from database.session import get_db, test_connection, engine
from database.models import Base, ContactMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nithin Dharavath - Portfolio")

app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"


@app.on_event("startup")
async def startup():
    if test_connection():
        Base.metadata.create_all(bind=engine)
        logger.info("Database connection successful.")
    else:
        logger.warning("Database connection failed — contact form will not work.")


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse((TEMPLATES_DIR / "index.html").read_text(encoding="utf-8"))


@app.get("/skills", response_class=HTMLResponse)
async def skills():
    return HTMLResponse((TEMPLATES_DIR / "skills.html").read_text(encoding="utf-8"))


@app.get("/privacy", response_class=HTMLResponse)
async def privacy():
    return HTMLResponse((TEMPLATES_DIR / "privacy.html").read_text(encoding="utf-8"))


@app.get("/terms", response_class=HTMLResponse)
async def terms():
    return HTMLResponse((TEMPLATES_DIR / "terms.html").read_text(encoding="utf-8"))


@app.post("/api/contact")
async def contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db),
):
    contact_rate_limiter.check(request)
    errors = []
    if not name.strip():
        errors.append("Name is required.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()):
        errors.append("A valid email is required.")
    if not subject.strip():
        errors.append("Subject is required.")
    if not message.strip():
        errors.append("Message is required.")

    if errors:
        return JSONResponse({"ok": False, "errors": errors}, status_code=422)

    try:
        entry = ContactMessage(
            name=name.strip(),
            email=email.strip(),
            subject=subject.strip(),
            message=message.strip(),
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        logger.info("Contact message saved: id=%s, email=%s", entry.id, entry.email)
        return JSONResponse({"ok": True, "message": "Message sent successfully!"})
    except Exception as e:
        db.rollback()
        logger.error("Failed to save contact message: %s", e)
        return JSONResponse(
            {"ok": False, "message": "Something went wrong. Please try again."},
            status_code=500,
        )
