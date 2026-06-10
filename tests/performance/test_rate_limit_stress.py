import time
from middleware.rate_limit import RateLimiter


class TestRateLimitPerformance:
    def test_high_frequency_requests(self):
        limiter = RateLimiter(max_requests=1000, window_seconds=60)
        n_requests = 1000
        start = time.perf_counter()
        req = _make_mock_request()
        for _ in range(n_requests):
            limiter.check(req)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0

    def test_multiple_ips_no_block(self):
        limiter = RateLimiter(max_requests=1, window_seconds=60)
        start = time.perf_counter()
        for i in range(1000):
            req = _make_mock_request(f"10.0.0.{i}")
            limiter.check(req)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0

    def test_cleanup_large_dataset(self):
        limiter = RateLimiter(max_requests=10000, window_seconds=1)
        for i in range(1000):
            req = _make_mock_request(f"10.0.0.{i % 256}")
            try:
                limiter.check(req)
            except Exception:
                pass
        start = time.perf_counter()
        limiter._cleanup()
        elapsed = time.perf_counter() - start
        assert elapsed < 0.5


def _make_mock_request(ip="127.0.0.1"):
    import types

    req = types.SimpleNamespace()
    req.client = types.SimpleNamespace()
    req.client.host = ip
    return req
