import os
import time
from collections import defaultdict

from fastapi import HTTPException, Request


class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        env_limit = os.getenv("CONTACT_RATE_LIMIT")
        env_window = os.getenv("CONTACT_RATE_WINDOW")
        self.max_requests = int(env_limit) if env_limit is not None else max_requests
        self.window_seconds = int(env_window) if env_window is not None else window_seconds
        self._clients: dict[str, list[float]] = defaultdict(list)
        self._cleanup_interval = 300
        self._last_cleanup = time.monotonic()

    def _get_client_ip(self, request: Request) -> str:
        forwarded = getattr(request, "headers", None)
        if forwarded is not None:
            forwarded_val = forwarded.get("X-Forwarded-For")
            if forwarded_val:
                return forwarded_val.split(",")[0].strip()
        if request.client:
            return request.client.host
        return "unknown"

    def _cleanup(self) -> None:
        now = time.monotonic()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        cutoff = now - self.window_seconds
        for ip in list(self._clients.keys()):
            self._clients[ip] = [t for t in self._clients[ip] if t > cutoff]
            if not self._clients[ip]:
                del self._clients[ip]
        self._last_cleanup = now

    def check(self, request: Request) -> None:
        self._cleanup()
        ip = self._get_client_ip(request)
        now = time.monotonic()
        cutoff = now - self.window_seconds
        timestamps = self._clients[ip]
        timestamps[:] = [t for t in timestamps if t > cutoff]
        if len(timestamps) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )
        timestamps.append(now)


contact_rate_limiter = RateLimiter()
