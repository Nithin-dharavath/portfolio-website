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
    assert "/health" in routes


def test_static_mount_exists():
    mounts = [r for r in app.routes if getattr(r, "name", None) == "static"]
    static_mount = next(iter(mounts), None)
    assert static_mount is not None
    assert str(static_mount.path) == "/static"


@pytest.mark.asyncio
@patch("main.test_connection")
async def test_startup_success_logs(mock_test_conn):
    mock_test_conn.return_value = True
    from main import lifespan

    async with lifespan(app):
        pass

    mock_test_conn.assert_called_once()


@pytest.mark.asyncio
@patch("main.test_connection")
async def test_startup_failure_logs(mock_test_conn):
    mock_test_conn.return_value = False
    from main import lifespan

    async with lifespan(app):
        pass

    mock_test_conn.assert_called_once()


@pytest.mark.asyncio
@patch("main.test_connection")
async def test_health_endpoint_ok(mock_test_conn, client):
    mock_test_conn.return_value = True
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"


@pytest.mark.asyncio
@patch("main.test_connection")
async def test_health_endpoint_degraded(mock_test_conn, client):
    mock_test_conn.return_value = False
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "degraded"
    assert data["database"] == "disconnected"
