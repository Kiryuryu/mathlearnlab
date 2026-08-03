"""Tests for the rate limiter — pure in-memory, no network."""

from server.services import ratelimit


def test_not_blocked_initially():
    assert not ratelimit.is_blocked("1.2.3.4")


def test_block_after_max_attempts():
    ip = "5.6.7.8"
    for _ in range(ratelimit._MAX_ATTEMPTS):
        ratelimit.record_failure(ip)
    assert ratelimit.is_blocked(ip)


def test_success_resets():
    ip = "9.9.9.9"
    for _ in range(ratelimit._MAX_ATTEMPTS - 1):
        ratelimit.record_failure(ip)
    ratelimit.record_success(ip)
    assert not ratelimit.is_blocked(ip)


def test_different_ips_independent():
    ratelimit.record_failure("10.0.0.1")
    for _ in range(ratelimit._MAX_ATTEMPTS - 1):
        ratelimit.record_failure("10.0.0.1")
    assert ratelimit.is_blocked("10.0.0.1")
    assert not ratelimit.is_blocked("10.0.0.2")
