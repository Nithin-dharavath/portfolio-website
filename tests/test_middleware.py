import time
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, Request

from middleware.rate_limit import RateLimiter, contact_rate_limiter


class TestRateLimiterInstance:
    def test_contact_rate_limiter_is_rate_limiter(self):
        assert isinstance(contact_rate_limiter, RateLimiter)

    def test_contact_rate_limiter_default_limits(self):
        assert contact_rate_limiter.max_requests == 5
        assert contact_rate_limiter.window_seconds == 60

    def test_contact_rate_limiter_initial_state(self):
        assert hasattr(contact_rate_limiter, "_clients")
        assert hasattr(contact_rate_limiter, "_last_cleanup")
        assert hasattr(contact_rate_limiter, "_cleanup_interval")


class TestRateLimiterEdgeCases:
    def make_request(self, ip: str = "10.0.0.1") -> MagicMock:
        req = MagicMock(spec=Request)
        req.client.host = ip
        return req

    def test_zero_max_requests(self):
        limiter = RateLimiter(max_requests=0, window_seconds=60)
        req = self.make_request()
        with pytest.raises(HTTPException) as exc:
            limiter.check(req)
        assert exc.value.status_code == 429

    def test_large_window(self):
        limiter = RateLimiter(max_requests=1000, window_seconds=3600)
        req = self.make_request()
        for _ in range(1000):
            limiter.check(req)
        with pytest.raises(HTTPException):
            limiter.check(req)

    def test_consecutive_requests_same_ip(self):
        limiter = RateLimiter(max_requests=100, window_seconds=60)
        req = self.make_request()
        for _ in range(100):
            limiter.check(req)

    def test_cleanup_interval_threshold(self):
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        initial = limiter._last_cleanup
        limiter._cleanup()
        assert limiter._last_cleanup == initial

    def test_cleanup_runs_when_interval_passed(self):
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        limiter._cleanup_interval = 0
        limiter._last_cleanup = time.monotonic() - 10
        limiter._cleanup()
        assert limiter._last_cleanup > time.monotonic() - 1

    async def test_rate_limiter_integration(self, client_with_rate_limit):
        resp = await client_with_rate_limit.post(
            "/api/contact",
            data={
                "name": "Test",
                "email": "test@test.com",
                "subject": "Test",
                "message": "Test",
            },
        )
        assert resp.status_code == 200
