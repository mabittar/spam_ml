import logging
from typing import List

from starlette.requests import Request
from starlette.responses import Response
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from fastapi import APIRouter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["health_check"])

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
@router.get(
    "/health_check",
    status_code=200,
    description="If this endpoint stops respond, k8s will kill the pod",
)
async def health_check(req: Request) -> Response:
    return Response(status_code=200)


@router.get(
    "/all_routes", description="List all available routes"
)
async def get_all_routes(req: Request) -> List[str]:
    # Using FastAPI instance
    url_list = [{"path": route.path, "name": route.name} for route in req.app.routes]
    return url_list
