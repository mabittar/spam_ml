import logging
from functools import lru_cache

from fastapi import APIRouter

from app.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["root"])


@lru_cache()
@router.get("/")
async def root():
    settings = Settings()
    msg = f"Hello visitant, {vars(settings)}!" if not settings.BIND_ENV else "Hello visitant!"
    return f'''
    <!Doctype html>
        <html>
            <body>
                <h1>SecureAPI</h1>
                    <div class="btn-group">
                        <a href="/docs"><button>SwaggerUI</button></a>
                        <a href="/redoc"><button>Redoc</button></a>
                    </div>
                <p>Hello visitant, {msg}!</p>
            </body>
        </html>
        '''

