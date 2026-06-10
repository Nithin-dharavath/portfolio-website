import time
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException, Request

from middleware.rate_limit import RateLimiter


class TestRateLimiterInit:
    def test_default_values(self):
        limiter = RateLimiter()
        assert limiter.max_requests == 5
        assert limiter.window_seconds == 60
        assert limiter._clients == {}

    def test_custom_values(self):
        limiter = RateLimiter(max_requests=10, window_seconds=30)
        assert limiter.max_requests == 10
        assert limiter.window_seconds == 30


class TestRateLimiterCheck:
    def make_request(self, ip: str = "192.168.1.1") -> MagicMock:
        req = MagicMock(spec=Request)
        req.client.host = ip
        return req

    def test_allows_under_limit(self):
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        req = self.make_request()
        for _ in range(5):
            limiter.check(req)

    def test_blocks_over_limit(self):
        limiter = RateLimiter(max_requests=3, window_seconds=60)
        req = self.make_request()
        for _ in range(3):
            limiter.check(req)
        with pytest.raises(HTTPException) as exc:
            limiter.check(req)
        assert exc.value.status_code == 429
        assert "Too many requests" in exc.value.detail

    def test_different_ips_separate_counters(self):
        limiter = RateLimiter(max_requests=1, window_seconds=60)
        req1 = self.make_request("192.168.1.1")
        req2 = self.make_request("192.168.1.2")
        limiter.check(req1)
        limiter.check(req2)
        with pytest.raises(HTTPException):
            limiter.check(req1)

    def test_blocks_at_exact_limit(self):
        limiter = RateLimiter(max_requests=2, window_seconds=60)
        req = self.make_request()
        limiter.check(req)
        limiter.check(req)
        with pytest.raises(HTTPException):
            limiter.check(req)

    def test_unknown_client(self):
        limiter = RateLimiter(max_requests=1, window_seconds=60)
        req = MagicMock(spec=Request)
        req.client = None
        limiter.check(req)
        with pytest.raises(HTTPException):
            limiter.check(req)


class TestRateLimiterCleanup:
    def make_request(self, ip: str = "192.168.1.1") -> MagicMock:
        req = MagicMock(spec=Request)
        req.client.host = ip
        return req

    def _make_cleanable_limiter(self, max_requests=5, window_seconds=1):
        limiter = RateLimiter(max_requests=max_requests, window_seconds=window_seconds)
        limiter._cleanup_interval = 0
        return limiter

    def test_cleanup_removes_old_entries(self):
        limiter = self._make_cleanable_limiter(window_seconds=1)
        req = self.make_request()
        limiter.check(req)
        time.sleep(1.1)
        limiter._cleanup()
        assert len(limiter._clients) == 0

    def test_cleanup_does_not_remove_fresh_entries(self):
        limiter = self._make_cleanable_limiter(window_seconds=60)
        req = self.make_request()
        limiter.check(req)
        limiter._cleanup()
        assert len(limiter._clients) == 1

    def test_cleanup_removes_empty_ip_keys(self):
        limiter = self._make_cleanable_limiter(max_requests=1, window_seconds=0.5)
        req = self.make_request()
        limiter.check(req)
        time.sleep(0.6)
        limiter._cleanup()
        assert len(limiter._clients) == 0

    def test_cleanup_does_not_run_before_interval(self):
        limiter = RateLimiter(max_requests=5, window_seconds=60)
        limiter._cleanup_interval = 999
        limiter._last_cleanup = time.monotonic()
        req = self.make_request()
        limiter.check(req)
        assert len(limiter._clients) == 1
