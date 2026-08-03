"""
Simple in-memory rate limiter for auth endpoints.
Tracks failed attempts per IP within a sliding window.
"""

import time

# {ip: [timestamps]}
_attempts: dict[str, list[float]] = {}
_WINDOW = 300  # 5 minutes
_MAX_ATTEMPTS = 10


def is_blocked(ip: str) -> bool:
    now = time.time()
    timestamps = _attempts.get(ip, [])
    timestamps = [t for t in timestamps if now - t < _WINDOW]
    _attempts[ip] = timestamps
    return len(timestamps) >= _MAX_ATTEMPTS


def record_failure(ip: str):
    now = time.time()
    timestamps = _attempts.get(ip, [])
    timestamps = [t for t in timestamps if now - t < _WINDOW]
    timestamps.append(now)
    _attempts[ip] = timestamps


def record_success(ip: str):
    _attempts.pop(ip, None)
