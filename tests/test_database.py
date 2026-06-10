import database.session
from unittest.mock import patch, MagicMock

from database.config import DB_CONFIG, DATABASE_URL


class TestDatabaseConfig:
    def test_db_config_keys(self):
        expected = {"host", "port", "database", "user", "password"}
        assert expected.issubset(DB_CONFIG.keys())

    def test_db_config_values(self):
        assert isinstance(DB_CONFIG.get("host"), (str, type(None)))
        assert isinstance(DB_CONFIG.get("port"), (int, type(None)))
        assert isinstance(DB_CONFIG.get("database"), (str, type(None)))
        assert isinstance(DB_CONFIG.get("user"), (str, type(None)))
        assert isinstance(DB_CONFIG.get("password"), (str, type(None)))

    def test_database_url_is_string(self):
        assert isinstance(DATABASE_URL, str)
        assert DATABASE_URL.startswith("mysql+pymysql://")


class TestDatabaseSession:
    @patch("database.session.SessionLocal")
    def test_get_db_creates_session(self, mock_session_local):
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session
        gen = database.session.get_db()
        session = next(gen)
        assert session is mock_session
        gen.close()
        mock_session.close.assert_called_once()

    @patch("database.session.test_connection")
    def test_test_connection_success(self, mock_test):
        mock_test.return_value = True
        assert database.session.test_connection() is True

    @patch("database.session.test_connection")
    def test_test_connection_failure(self, mock_test):
        mock_test.return_value = False
        assert database.session.test_connection() is False

    @patch("database.session.engine.connect")
    def test_test_connection_engine_success(self, mock_connect):
        mock_connect.return_value.__enter__.return_value = MagicMock()
        result = database.session.test_connection()
        assert result is True

    @patch("database.session.engine.connect")
    def test_test_connection_engine_failure(self, mock_connect):
        mock_connect.side_effect = Exception("Connection refused")
        result = database.session.test_connection()
        assert result is False

    @patch("database.session.engine.connect")
    def test_test_connection_executes_select_1(self, mock_connect):
        mock_conn = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        database.session.test_connection()
        mock_conn.execute.assert_called_once()
        call_args = mock_conn.execute.call_args[0][0]
        assert "SELECT 1" in str(call_args)


class TestDatabaseModels:
    def test_model_creates_and_queries(self, db_session):
        from database.models import ContactMessage

        msg = ContactMessage(
            name="Test",
            email="test@test.com",
            subject="Test Subject",
            message="Test Message",
        )
        db_session.add(msg)
        db_session.commit()
        retrieved = db_session.query(ContactMessage).first()
        assert retrieved is not None
        assert retrieved.name == "Test"
        assert retrieved.email == "test@test.com"

    def test_model_increments_ids(self, db_session):
        from database.models import ContactMessage

        for i in range(5):
            msg = ContactMessage(
                name=f"User {i}",
                email=f"user{i}@test.com",
                subject="Test",
                message="Test",
            )
            db_session.add(msg)
            db_session.commit()
        msgs = db_session.query(ContactMessage).all()
        assert len(msgs) == 5
        ids = [m.id for m in msgs]
        assert ids == list(range(1, 6))

    def test_model_created_at_is_set(self, db_session):
        from database.models import ContactMessage

        msg = ContactMessage(
            name="Test",
            email="test@test.com",
            subject="Test",
            message="Test",
        )
        db_session.add(msg)
        db_session.commit()
        assert msg.created_at is not None

    def test_model_rollback(self, db_session):
        from database.models import ContactMessage

        msg = ContactMessage(
            name="Rollback Test",
            email="rollback@test.com",
            subject="Test",
            message="Test",
        )
        db_session.add(msg)
        db_session.rollback()
        count = db_session.query(ContactMessage).count()
        assert count == 0

    def test_model_delete(self, db_session):
        from database.models import ContactMessage

        msg = ContactMessage(
            name="Delete Test",
            email="delete@test.com",
            subject="Test",
            message="Test",
        )
        db_session.add(msg)
        db_session.commit()
        db_session.delete(msg)
        db_session.commit()
        count = db_session.query(ContactMessage).count()
        assert count == 0

    def test_model_bulk_insert(self, db_session):
        from database.models import ContactMessage

        entries = [
            ContactMessage(
                name=f"User {i}", email=f"u{i}@t.com", subject="S", message="M"
            )
            for i in range(10)
        ]
        for e in entries:
            db_session.add(e)
        db_session.commit()
        count = db_session.query(ContactMessage).count()
        assert count == 10
