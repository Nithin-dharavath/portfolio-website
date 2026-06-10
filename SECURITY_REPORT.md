# Security Report

**Date:** 2026-06-10
**Project:** Nithin Dharavath - Portfolio (FastAPI)

---

## Summary

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| Before | 0 | 0 | 0 | 0 |
| After | 0 | 0 | 0 | 1 (test code) |

**Vulnerable Dependencies (Before):** 6 CVEs in 2 packages
**Vulnerable Dependencies (After):** 0 CVEs

---

## Dependency Vulnerabilities Fixed

### `python-dotenv` 1.1.0 → 1.2.2
- **CVE-2026-28684** — Fixed

### `setuptools` 65.5.0 → 82.0.1
- **PYSEC-2022-43012** — Fixed
- **PYSEC-2025-49** — Fixed
- **CVE-2024-6345** — Fixed

---

## Security Improvements Applied

### 1. Security Headers Middleware (`middleware/__init__.py`)
Added `SecurityHeadersMiddleware` that sets on all responses:
- `X-Content-Type-Options: nosniff` — Prevents MIME type sniffing
- `X-Frame-Options: DENY` — Prevents clickjacking
- `X-XSS-Protection: 1; mode=block` — Enables browser XSS filtering
- `Referrer-Policy: strict-origin-when-cross-origin` — Controls referrer information
- `Permissions-Policy: camera=(), microphone=(), geolocation=()` — Restricts browser features

### 2. Input Validation Hardening (`main.py`)
- **Max length limits:** Name (100), Email (255), Subject (255), Message (10000)
- **Stronger email regex:** `^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$` instead of weak `[^@]+@[^@]+\.[^@]+`
- **Pre-validation stripping:** Input stripped before validation to prevent bypass

### 3. Sensitive Data Protection (`main.py`)
- Removed email address from contact save log message — prevents PII in logs
- Uses `logger.exception()` instead of `logger.error(e)` — cleaner stack traces without string interpolation

### 4. Dependency Updates (`requirements.txt`)
- Updated `python-dotenv` from 1.1.0 to 1.2.2
- Updated `setuptools` (transitive) from 65.5.0 to 82.0.1

---

## Security Audit Results

### Bandit Scan (Project Code Only)

| Severity | Count | Details |
|----------|-------|---------|
| High | 0 | — |
| Medium | 0 | — |
| Low | 1 | `try_except_pass` in `tests/performance/test_rate_limit_stress.py:31` |

**Note:** The single low-severity finding is in test code where catching all exceptions is intentional for performance benchmarking.

### pip-audit Results

```
No known vulnerabilities found
```

### Authentication
- N/A — No authentication system (portfolio contact form only)

### Authorization
- N/A — No role-based access control needed

### Input Validation
- ✅ SQL Injection: Protected — SQLAlchemy ORM with parameterized queries
- ✅ XSS: Protected — HTML templates served as static files, form data validated
- ✅ Command Injection: Not applicable — no shell commands
- ✅ Path Traversal: Protected — StaticFiles serves only from `static/` directory
- ✅ SSRF: Not applicable — no outbound HTTP requests from user input
- ✅ Deserialization: Not applicable — no pickle/YAML deserialization of user input

### API Security
- ✅ Rate limiting: 5 requests per 60 seconds per IP on `/api/contact`
- ✅ Input validation: All form fields validated for presence, type, and length
- ✅ Error responses: Generic error messages, no internal details leaked
- ✅ Method restrictions: POST-only for contact form

### Secrets Management
- ✅ `.env` file in `.gitignore` — not committed to repository
- ✅ No hardcoded credentials in source code
- ✅ Database credentials loaded from environment variables

### Database Security
- ✅ SQLAlchemy ORM — no raw SQL queries
- ✅ Parameterized queries — no string interpolation in SQL
- ✅ Session management — proper cleanup in finally block

### CORS
- Not configured — acceptable for a single-origin portfolio site. If API access from other origins is needed later, configure explicit allowed origins.

---

## Remaining Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| No CSRF protection on contact form | Low | Rate limiting provides partial mitigation. Add CSRF tokens if form is embedded in third-party sites. |
| No HTTPS enforcement | Low | Should be handled at reverse proxy/deployment level (e.g., nginx, Cloudflare) |
| No Content-Security-Policy header | Low | Consider adding CSP if inline scripts are added in the future |
| Rate limiter uses in-memory storage | Low | Resets on server restart. Use Redis for production multi-instance deployments |

---

## Recommendations

1. **Add HTTPS enforcement** at the reverse proxy level
2. **Consider CSP headers** if adding inline scripts or third-party resources
3. **Use Redis for rate limiting** if deploying multiple instances
4. **Add CSRF tokens** if the contact form is embedded in other sites
5. **Regular dependency updates** — run `pip-audit` in CI/CD pipeline

---

## Commands Used

```bash
bandit -r . --skip B101 --exclude ./venv  # 0 project issues, 1 low in tests
pip-audit                                  # No known vulnerabilities
```
