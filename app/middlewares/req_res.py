import logging
import time
from typing import Callable

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerfTimer(BaseHTTPMiddleware):
    def __init__(self, app: Starlette):
        super().__init__(app)
        self.__start_time = None

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request = await self.time_starter(request=request)
        response = await call_next(request)
        response = await self.time_stopper(request=request, response=response)
        return response

    async def time_starter(self, request: Request) -> Request:
        self.__start_time = time.perf_counter()
        logger.info(f"REQUEST {request.method.upper()} {request.url.path}")
        return request

    async def time_stopper(self, request: Request, response: Response) -> Response:
        took = time.perf_counter() - self.__start_time
        str_took = '{:0.4f}'.format(took * 1000)
        logger.info(f"RESPONSE {request.method.upper()} {request.url.path} response time: {str_took} ms")
        return response
