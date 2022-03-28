
from traceback import format_exc
from urllib.error import HTTPError
from urllib.request import Request

from settings import PROJECT_NAME
from fastapi import FastAPI

from starlette.responses import JSONResponse

from endpoints.user import router as user_endpoint
from endpoints.health_check import router as health_check_endpoint
from infrastructure.error_handler import ErrorMessage


app = FastAPI(title=PROJECT_NAME, docs_url=f"/docs/")


app.include_router(health_check_endpoint, tags=["health_check"])
app.include_router(user_endpoint, prefix="/users", tags=["user"])


@app.exception_handler(HTTPError)
async def http_error_handler(request: Request, exception: HTTPError):
    if exception.detail:
        return JSONResponse(
            status_code=exception.detail.get("http_status", 500),
            content={**exception.detail, **{"code": exception.code}},
        )
    else:
        str_tb = format_exc()
        msg = ErrorMessage(
            traceback=str_tb,
            title="Some error occur",
            code=exception.code,
            http_status="500"

        )
        return JSONResponse(status_code=msg.http_status, content={**msg.dict()})

if __name__ == '__main__':
    from uvicorn import run
    from settings import HOST, PORT

    run(app,  # type: ignore
        port=PORT,
        host=HOST,
        use_colors=True
        )

