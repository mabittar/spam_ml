import logging
import time
from typing import Callable

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestResponse(BaseHTTPMiddleware):
    def __init__(self, app: Starlette):
        super().__init__(app)
        self.__start_time = None

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request = await self.process_request(request=request)
        response = await call_next(request)
        response = await self.process_response(request=request, response=response)
        return response

    async def process_request(self, request: Request) -> Request:
        self.__start_time = time.perf_counter()
        logger.info(f"REQUEST {request.method.upper()} {request.url.path}")
        return request

    async def process_response(self, request: Request, response: Response) -> Response:
        took = time.perf_counter() - self.__start_time
        str_took = str(('{0.4:f}'.format(took)))
        logger.info(f"RESPONSE {request.method.upper()} {request.url.path} took: {str_took}")
        return response
