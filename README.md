# Nithin Dharavath — Portfolio

A professional portfolio website built with FastAPI, featuring a responsive design, contact form, and comprehensive testing.

## Tech Stack

| Layer      | Technology                                |
| ---------- | ----------------------------------------- |
| Backend    | Python 3.11+, FastAPI, Uvicorn, Gunicorn |
| Database   | MySQL (TiDB Cloud) via SQLAlchemy/PyMySQL |
| Frontend   | Semantic HTML, CSS, Vanilla JS            |
| Testing    | pytest, pytest-asyncio                   |
| Deployment | Vercel                                    |

## Project Structure

```
├── api/
│   └── index.py         # Vercel serverless entry point
├── main.py              # FastAPI app entry point
├── database/            # DB config, session, models, init.sql
├── middleware/          # Security headers, rate limiting
├── static/
│   ├── css/             # style.css, skills.css, privacy.css, terms.css
│   ├── js/              # main.js, skills.js
│   ├── resume/          # Resume downloads
│   ├── robots.txt       # Crawler instructions
│   └── og-image.svg     # Social preview image
├── templates/           # index.html, skills.html, privacy.html, terms.html
├── tests/               # Unit, integration, e2e, performance tests
├── vercel.json
└── requirements.txt
```

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL-compatible database (or TiDB Cloud)

### Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your database credentials
```

### Run

```bash
# Development
uvicorn main:app --reload

# Production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

Open [http://localhost:8000](http://localhost:8000).

## Routes

| Path         | Description        |
| ------------ | ------------------ |
| `/`          | Home page          |
| `/skills`    | Skills page        |
| `/privacy`   | Privacy policy     |
| `/terms`     | Terms of service   |
| `/api/contact` | Contact form (POST) |
| `/health`    | Health check       |

## Testing

```bash
pytest                       # All tests
pytest -v                    # Verbose
pytest --cov=. --cov-report=term  # With coverage
```

## Deployment

The project is deployed on Vercel. The `api/index.py` file serves as the serverless entry point. Key environment variables:

| Variable      | Description                    |
| ------------- | ------------------------------ |
| `DB_HOST`     | Database host                  |
| `DB_PORT`     | Database port                  |
| `DB_NAME`     | Database name                  |
| `DB_USER`     | Database user                  |
| `DB_PASSWORD` | Database password              |
| `PORT`     | Application port (default 8000, not needed on Vercel) |

## Code Quality

| Check    | Status |
| -------- | ------ |
| Ruff     | 0 errors |
| Mypy     | 0 errors |
| Black    | 0 issues |
| Bandit   | 0 issues |
| Tests    | 112 passing |

## License

MIT
