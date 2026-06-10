class TestPortfolioBrowsing:
    async def test_visit_homepage(self, client):
        resp = await client.get("/")
        assert resp.status_code == 200
        text = resp.text
        assert "Nithin Dharavath" in text
        assert "Backend Developer" in text
        assert "Contact" in text

    async def test_visit_skills_page(self, client):
        resp = await client.get("/skills")
        assert resp.status_code == 200
        text = resp.text
        assert "Skills" in text
        assert "Python" in text
        assert "FastAPI" in text

    async def test_visit_privacy(self, client):
        resp = await client.get("/privacy")
        assert resp.status_code == 200
        assert resp.status_code == 200

    async def test_visit_terms(self, client):
        resp = await client.get("/terms")
        assert resp.status_code == 200


class TestContactWorkflow:
    async def test_submit_contact_form(self, client):
        resp = await client.post(
            "/api/contact",
            data={
                "name": "Diana Prince",
                "email": "diana@example.com",
                "subject": "Project Collaboration",
                "message": "I'd like to discuss a backend project.",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert "sent successfully" in data["message"].lower()

    async def test_submit_invalid_email(self, client):
        resp = await client.post(
            "/api/contact",
            data={
                "name": "Diana",
                "email": "not-an-email",
                "subject": "Test",
                "message": "Test message",
            },
        )
        assert resp.status_code == 422
        data = resp.json()
        assert data["ok"] is False

    async def test_submit_empty_form(self, client):
        resp = await client.post(
            "/api/contact",
            data={"name": "", "email": "", "subject": "", "message": ""},
        )
        assert resp.status_code == 422
        data = resp.json()
        assert len(data["errors"]) == 4
