import logging
from functools import lru_cache

from fastapi import APIRouter

from app.settings import Settings
from yattag import Doc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["root"])


@lru_cache()
@router.get("/")
async def root():
    settings = Settings()
    doc, tag, text, line = Doc(
        defaults={
            'title': "Spam ML in FastAPI"
        }
    ).ttl()
    doc.asis('<!DOCTYPE html>')
    msg = f"Hello visitant, {vars(settings)}!" if not settings.BIND_ENV else "Hello visitant!"
    line("h1", "This is a Secure API you need to create a login to use the app.")
    with tag("html"):
        doc.input(name="title", type="text")
        with tag("body"):
            with tag("h1", id="header"):
                text()
            with tag("button", id="btn-group"):
                with tag("a", href='/docs'):
                    text("SwaggerUI")
                with tag("a", href='/redoc'):
                    text("Redoc")
            with tag("p", id="footer"):
                text(f"Hello visitant, {msg}!")

    result = doc.getvalue()

    return result


