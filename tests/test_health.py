import pytest
from unittest.mock import patch

from main import app


def test_app_title():
    assert app.title == "Nithin Dharavath - Portfolio"


def test_app_routes_loaded():
    routes = [r.path for r in app.routes]
    assert "/" in routes
    assert "/skills" in routes
    assert "/privacy" in routes
    assert "/terms" in routes
    assert "/api/contact" in routes


def test_static_mount_exists():
    mounts = [r for r in app.routes if getattr(r, "name", None) == "static"]
    static_mount = next(iter(mounts), None)
    assert static_mount is not None
    assert str(static_mount.path) == "/static"


@pytest.mark.asyncio
@patch("main.test_connection")
@patch("main.Base.metadata.create_all")
async def test_startup_success_creates_tables(mock_create_all, mock_test_conn):
    mock_test_conn.return_value = True
    from main import lifespan

    async with lifespan(app):
        mock_create_all.assert_called_once()


@pytest.mark.asyncio
@patch("main.test_connection")
@patch("main.Base.metadata.create_all")
async def test_startup_failure_skips_tables(mock_create_all, mock_test_conn):
    mock_test_conn.return_value = False
    from main import lifespan

    async with lifespan(app):
        mock_create_all.assert_not_called()
