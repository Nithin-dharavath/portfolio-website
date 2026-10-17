# Nithin Dharavath — AI Engineer Portfolio

A production-ready portfolio website engineered with FastAPI, featuring an interactive 3D Three.js canvas, responsive design, contact pipeline, comprehensive test suite, and advanced Search Engine Optimization (SEO) linking to GitHub and LinkedIn.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nithin_Dharavath-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/nithin-dharavathu/)
[![GitHub](https://img.shields.io/badge/GitHub-Nithin--dharavath-181717?style=flat&logo=github)](https://github.com/Nithin-dharavath)
[![Email](https://img.shields.io/badge/Email-Contact_Nithin-EA4335?style=flat&logo=gmail)](mailto:nithindharavath01@gmail.com)
[![Tests](https://img.shields.io/badge/Tests-122%20passing-success)](tests/)

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| **Backend** | Python 3.11+, FastAPI, Uvicorn, Gunicorn |
| **Database** | MySQL (TiDB Cloud) via SQLAlchemy & PyMySQL |
| **Frontend** | Semantic HTML5, CSS3 Variables, Vanilla JS, Three.js 3D Canvas |
| **SEO & Identity** | Schema.org JSON-LD Graph (`Person`, `ProfilePage`, `WebSite`), Open Graph, Twitter Cards, `rel="me"` |
| **Testing** | pytest, pytest-asyncio, pytest-cov, pytest-mock (122 tests) |
| **Deployment** | Vercel (Serverless ASGI Entrypoint) |

---

## SEO & Search Visibility Optimization

The application is specifically engineered for search engines (Google, Bing, DuckDuckGo) to discover, index, and associate searches for **Nithin Dharavath**, **Nithin Dharavathu**, and queries like `Nithin Dharavath LinkedIn` or `Nithin Dharavath GitHub` directly with this portfolio:

1. **Schema.org JSON-LD `@graph`**:
   - `Person` schema with `sameAs` referencing official GitHub (`https://github.com/Nithin-dharavath`) and LinkedIn (`https://www.linkedin.com/in/nithin-dharavathu/`) profiles.
   - Alternate name variations (`Nithin Dharavathu`, `Nithin-dharavath`).
   - `ProfilePage` structured data indicating the page's primary entity as recommended by Google Search Central.
   - `WebSite` structured data with author/publisher entity bindings.

2. **Bidirectional Identity Verification (`rel="me"`)**:
   - Navigation, contact section, and footer links to GitHub and LinkedIn utilize `rel="me noopener noreferrer"` for verified social profile linkage.

3. **Open Graph & Twitter Cards**:
   - `og:see_also` pointing directly to GitHub and LinkedIn profiles.
   - Profile Open Graph meta properties (`profile:first_name`, `profile:last_name`, `profile:username`).
   - Absolute image URLs for preview cards across LinkedIn, X/Twitter, and messaging platforms.

4. **Crawler Indexing**:
   - Root `/robots.txt` route serving crawler directives and sitemap URL.
   - Dynamic XML sitemap at `/sitemap.xml` with page priorities and update frequencies.

---

## Project Structure

```
├── api/
│   └── index.py         # Vercel serverless ASGI entry point
├── database/            # Database configuration, models, session
│   ├── config.py
│   ├── init.sql
│   ├── models.py
│   └── session.py
├── middleware/          # Security headers and rate limiting
│   ├── __init__.py
│   └── rate_limit.py
├── static/
│   ├── css/             # style.css, skills.css, legal.css
│   ├── js/              # main.js, skills.js, three.min.js, three-scene.js
│   ├── resume/          # Resume PDF downloads
│   ├── favicon.ico      # Favicon
│   ├── favicon.svg      # Vector brand favicon
│   ├── og-image.svg     # Social preview image (1200x630)
│   ├── robots.txt       # Crawler instructions & sitemap link
│   └── sitemap.xml      # Search engine URL directory
├── templates/           # Jinja2 templates
│   ├── 404.html
│   ├── base.html        # Base layout with rich SEO <head> and Schema.org
│   ├── index.html       # Hero, 3D canvas, projects, contact form
│   ├── privacy.html     # Privacy policy
│   ├── skills.html      # Technical mastery & intelligence stack
│   └── terms.html       # Terms of service
├── tests/               # 122 unit, integration, e2e, and stress tests
├── main.py              # FastAPI application & route definitions
├── requirements.txt
└── pytest.ini
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL-compatible database (e.g., TiDB Cloud)

### Setup

```bash
# Clone the repository
git clone https://github.com/Nithin-dharavath/portfolio-website.git
cd portfolio-website

# Create and activate virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Create and activate virtual environment (macOS/Linux)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials
```

### Run Locally

```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Routes

| Path | Method | Description |
| --- | --- | --- |
| `/` | `GET` | Home page (3D hero, projects, about, contact) |
| `/skills` | `GET` | Comprehensive skills & intelligence stack |
| `/privacy` | `GET` | Privacy policy |
| `/terms` | `GET` | Terms of service |
| `/api/contact` | `POST` | Contact inquiry endpoint (rate-limited, validated) |
| `/health` | `GET` | Health check & database connectivity probe |
| `/robots.txt` | `GET` | Search engine crawler instructions |
| `/sitemap.xml` | `GET` | XML sitemap for search crawlers |
| `/favicon.ico` | `GET` | Favicon |

---

## Testing

The project maintains an asynchronous test suite covering models, database sessions, middleware security, contact forms, routes, rate limits, static files, and end-to-end workflows:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run with test coverage report
pytest --cov=. --cov-report=term
```

---

## Deployment

The application is deployed on Vercel using the serverless ASGI bridge in `api/index.py`.

Required environment variables:

| Variable | Description |
| --- | --- |
| `DB_HOST` | Database host (e.g. TiDB Cloud gateway) |
| `DB_PORT` | Database port (typically `4000` or `3306`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `MAX_REQUEST_SIZE` | Maximum body size in bytes (default: `1048576`) |

---

## Code Quality

| Quality Gate | Status |
| --- | --- |
| **Ruff** | 0 errors |
| **Mypy** | 0 type errors |
| **Security Headers** | CSP, HSTS, X-Content-Type-Options, Referrer-Policy |
| **Test Suite** | 122 passing tests |

---

## License

MIT &copy; 2026 [Nithin Dharavath](https://github.com/Nithin-dharavath)
