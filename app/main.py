from pathlib import Path
from typing import Annotated

from fastapi import FastAPI
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app.utils.anki_api import send_to_ankiweb
from app.utils.constants import AVAILABLE_LANGUAGES
from app.utils.image_fetcher import fetch_image_url
from app.utils.openai_client import generate_anki_fields
from app.utils.tts_client import generate_audio_files

app = FastAPI()

# Mount static files
app.mount(
    "/static",
    StaticFiles(directory=(Path(__file__).parent / "static")),
    name="static",
)

# Set up templates
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# Global exception handler for all errors
@app.exception_handler(Exception)  # type: ignore[misc]
async def global_exception_handler(request: Request, exc: Exception) -> Response:
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "error": str(exc)},
        status_code=500,
    )


@app.get("/", response_class=HTMLResponse)  # type: ignore[misc]
def get_form(request: Request) -> HTMLResponse:
    # Pass ALLOWED_LANGUAGES to the template
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "languages": AVAILABLE_LANGUAGES,
            "error": None,
            "confirmation": None,
            "preview": None,
        },
    )


@app.post("/generate", response_class=HTMLResponse)  # type: ignore[misc]
def generate_card(
    request: Request,
    word: Annotated[str, Form(...)],
    target_language: Annotated[str, Form(...)],
    translation_language: Annotated[str, Form(...)],
) -> HTMLResponse:
    try:
        fields = generate_anki_fields(
            word,
            target_language,
            translation_language,
        )
        image_url = fetch_image_url(word)
        audio_word, audio_sentence = generate_audio_files(fields)

        fields["Image"] = image_url
        fields["AudioWord"] = audio_word
        fields["AudioSentence"] = audio_sentence

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "preview": fields,
                "languages": AVAILABLE_LANGUAGES,
                "error": None,
                "confirmation": None,
            },
        )
    except Exception as exc:  # noqa: BLE001
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(exc),
                "languages": AVAILABLE_LANGUAGES,
                "confirmation": None,
                "preview": None,
            },
            status_code=500,
        )


@app.post("/submit", response_class=HTMLResponse)  # type: ignore[misc]
def submit_card(
    request: Request,
    word: Annotated[str, Form(...)],
    target_language: Annotated[str, Form(...)],
    translation_language: Annotated[str, Form(...)],
) -> HTMLResponse:
    try:
        fields = generate_anki_fields(word, target_language, translation_language)
        fields["Image"] = fetch_image_url(word)
        fields["AudioWord"], fields["AudioSentence"] = generate_audio_files(fields)
        send_to_ankiweb(fields)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "confirmation": True},
        )
    except Exception as exc:  # noqa: BLE001
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(exc)},
            status_code=500,
        )
