import pytest

VALID_PAYLOAD = {
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Project Inquiry",
    "message": "I would like to hire you for a project.",
}


class TestContactFormValid:
    async def test_valid_submission(self, client):
        response = await client.post("/api/contact", data=VALID_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert data["message"] == "Message sent successfully!"

    async def test_valid_submission_creates_record(self, client, db_session):
        await client.post("/api/contact", data=VALID_PAYLOAD)
        from database.models import ContactMessage

        count = db_session.query(ContactMessage).count()
        assert count == 1

    async def test_valid_submission_stores_correct_data(self, client, db_session):
        await client.post("/api/contact", data=VALID_PAYLOAD)
        from database.models import ContactMessage

        msg = db_session.query(ContactMessage).first()
        assert msg.name == "John Doe"
        assert msg.email == "john@example.com"
        assert msg.subject == "Project Inquiry"
        assert msg.message == "I would like to hire you for a project."
        assert msg.id is not None
        assert msg.created_at is not None

    async def test_strips_whitespace(self, client, db_session):
        payload = {k: f"  {v}  " for k, v in VALID_PAYLOAD.items()}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 200
        from database.models import ContactMessage

        msg = db_session.query(ContactMessage).first()
        assert msg.name == "John Doe"
        assert msg.email == "john@example.com"

    async def test_multiple_submissions(self, client, db_session):
        for i in range(3):
            payload = {**VALID_PAYLOAD, "name": f"User {i}"}
            response = await client.post("/api/contact", data=payload)
            assert response.status_code == 200
        from database.models import ContactMessage

        count = db_session.query(ContactMessage).count()
        assert count == 3


class TestContactFormValidation:
    @pytest.mark.parametrize("field", ["name", "email", "subject", "message"])
    async def test_missing_field(self, client, field):
        payload = {k: v for k, v in VALID_PAYLOAD.items() if k != field}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422
        data = response.json()
        assert data["ok"] is False
        assert len(data["errors"]) >= 1

    @pytest.mark.parametrize(
        "field,error_substring",
        [
            ("name", "Name"),
            ("email", "email"),
            ("subject", "Subject"),
            ("message", "Message"),
        ],
    )
    async def test_empty_field(self, client, field, error_substring):
        payload = {**VALID_PAYLOAD, field: ""}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422
        data = response.json()
        assert any(error_substring in e for e in data["errors"])

    async def test_all_empty_fields(self, client):
        payload = {"name": "", "email": "", "subject": "", "message": ""}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422
        data = response.json()
        assert len(data["errors"]) == 4

    async def test_invalid_email(self, client):
        payload = {**VALID_PAYLOAD, "email": "not-an-email"}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422
        data = response.json()
        assert any("email" in e.lower() for e in data["errors"])

    async def test_invalid_email_no_at(self, client):
        payload = {**VALID_PAYLOAD, "email": "userexample.com"}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422

    async def test_invalid_email_no_domain(self, client):
        payload = {**VALID_PAYLOAD, "email": "user@"}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422

    async def test_whitespace_only_fields(self, client):
        payload = {k: "   " for k in VALID_PAYLOAD}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 422
        data = response.json()
        assert len(data["errors"]) == 4

    async def test_large_message_body(self, client):
        payload = {**VALID_PAYLOAD, "message": "A" * 10000}
        response = await client.post("/api/contact", data=payload)
        assert response.status_code == 200


class TestContactFormErrors:
    async def test_database_error_returns_500(self, client):
        from unittest.mock import patch
        from sqlalchemy.orm import Session as SASession

        with patch.object(SASession, "commit", side_effect=Exception("DB Error")):
            response = await client.post("/api/contact", data=VALID_PAYLOAD)
            assert response.status_code == 500
            data = response.json()
            assert data["ok"] is False
            assert "Something went wrong" in data["message"]
