from sqlalchemy import Integer, String, Text, TIMESTAMP

from database.models import ContactMessage, Base


class TestContactMessageModel:
    def test_table_name(self):
        assert ContactMessage.__tablename__ == "contact_messages"

    def test_extends_base(self):
        assert issubclass(ContactMessage, Base)

    def test_id_column(self):
        col = ContactMessage.__table__.c["id"]
        assert isinstance(col.type, Integer)
        assert col.primary_key
        assert col.autoincrement is True or col.autoincrement == "auto"

    def test_name_column(self):
        col = ContactMessage.__table__.c["name"]
        assert isinstance(col.type, String)
        assert col.type.length == 100
        assert not col.nullable

    def test_email_column(self):
        col = ContactMessage.__table__.c["email"]
        assert isinstance(col.type, String)
        assert col.type.length == 255
        assert not col.nullable

    def test_subject_column(self):
        col = ContactMessage.__table__.c["subject"]
        assert isinstance(col.type, String)
        assert col.type.length == 255
        assert not col.nullable

    def test_message_column(self):
        col = ContactMessage.__table__.c["message"]
        assert isinstance(col.type, Text)
        assert not col.nullable

    def test_created_at_column(self):
        col = ContactMessage.__table__.c["created_at"]
        assert isinstance(col.type, TIMESTAMP)
        assert col.server_default is not None

    def test_all_columns_present(self):
        expected = {"id", "name", "email", "subject", "message", "created_at"}
        actual = set(ContactMessage.__table__.c.keys())
        assert actual == expected

    def test_contact_message_instantiation(self):
        msg = ContactMessage(
            name="Test User",
            email="test@example.com",
            subject="Test",
            message="Test message body",
        )
        assert msg.name == "Test User"
        assert msg.email == "test@example.com"
        assert msg.subject == "Test"
        assert msg.message == "Test message body"
        assert msg.id is None

    def test_repr(self):
        msg = ContactMessage(
            name="Test", email="test@test.com", subject="S", message="M"
        )
        assert "ContactMessage" in repr(msg)
