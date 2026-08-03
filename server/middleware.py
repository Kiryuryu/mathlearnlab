"""
Request logging middleware — logs method, path, status, and duration per request.
"""

import logging
import time

logger = logging.getLogger("mathlearnlab.access")


class RequestLogMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        start = time.time()
        method = scope.get("method", "?")
        path = scope.get("path", "?")
        status = 0

        async def send_wrapper(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            duration_ms = (time.time() - start) * 1000
            logger.info("%s %s -> %s (%dms)", method, path, status, round(duration_ms))
