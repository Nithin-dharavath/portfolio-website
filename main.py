import logging
import re
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Form, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from middleware import SecurityHeadersMiddleware
from middleware.rate_limit import contact_rate_limiter

from database.session import get_db, test_connection, engine
from database.models import Base, ContactMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 255
MAX_SUBJECT_LENGTH = 255
MAX_MESSAGE_LENGTH = 10000

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if test_connection():
        Base.metadata.create_all(bind=engine)
        logger.info("Database connection successful.")
    else:
        logger.warning("Database connection failed — contact form will not work.")
    yield


app = FastAPI(title="Nithin Dharavath - Portfolio", lifespan=lifespan)

app.add_middleware(SecurityHeadersMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")


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
    name: str = Form(""),
    email: str = Form(""),
    subject: str = Form(""),
    message: str = Form(""),
    db: Session = Depends(get_db),
):
    contact_rate_limiter.check(request)
    errors: list[str] = []

    name = name.strip()
    email = email.strip()
    subject = subject.strip()
    message = message.strip()

    if not name:
        errors.append("Name is required.")
    elif len(name) > MAX_NAME_LENGTH:
        errors.append(f"Name must be {MAX_NAME_LENGTH} characters or fewer.")

    if not email:
        errors.append("A valid email is required.")
    elif not EMAIL_REGEX.match(email):
        errors.append("A valid email is required.")
    elif len(email) > MAX_EMAIL_LENGTH:
        errors.append(f"Email must be {MAX_EMAIL_LENGTH} characters or fewer.")

    if not subject:
        errors.append("Subject is required.")
    elif len(subject) > MAX_SUBJECT_LENGTH:
        errors.append(f"Subject must be {MAX_SUBJECT_LENGTH} characters or fewer.")

    if not message:
        errors.append("Message is required.")
    elif len(message) > MAX_MESSAGE_LENGTH:
        errors.append(f"Message must be {MAX_MESSAGE_LENGTH} characters or fewer.")

    if errors:
        return JSONResponse({"ok": False, "errors": errors}, status_code=422)

    try:
        entry = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        logger.info("Contact message saved: id=%s", entry.id)
        return JSONResponse({"ok": True, "message": "Message sent successfully!"})
    except Exception:
        db.rollback()
        logger.exception("Failed to save contact message")
        return JSONResponse(
            {"ok": False, "message": "Something went wrong. Please try again."},
            status_code=500,
        )
