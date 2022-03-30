import asyncio
from functools import lru_cache

from fastapi import FastAPI
from traceback import format_exc
from urllib.error import HTTPError
from urllib.request import Request
from starlette.responses import JSONResponse

from .endpoints import health_check as health_check_endpoint
from .endpoints import user as user_endpoint
from settings import Settings
from .infrastructure.error_handler import ErrorMessage


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()


app = FastAPI(title=settings.PROJECT_NAME, docs_url=f"/docs/")

app.include_router(health_check_endpoint, tags=["health_check"])
app.include_router(user_endpoint, prefix="/users", tags=["user"])


@app.get("/")
def home():
    template = f'''
        <p>Hello, {vars(settings)}!</p>
        '''
    return template


@app.exception_handler(HTTPError)
async def http_error_handler(request: Request, exception: HTTPError):
    if exception.msg:
        return JSONResponse(
            status_code=exception.code,
            content={exception.__repr__},
        )
    else:
        str_tb = format_exc()
        msg = ErrorMessage(
            traceback=str_tb,
            title="Some error occur",
            code=exception.code

        )
        return JSONResponse(status_code=exception.code, content=msg.dict())

if __name__ == '__main__':
    from uvicorn import run

    run(app,  # type: ignore
        port=settings.PORT,
        host=settings.HOST,
        use_colors=True
        )

