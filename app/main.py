from typing import Annotated

from fastapi import FastAPI
from fastapi import Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.anki_api import send_to_ankiweb
from utils.image_fetcher import fetch_image_url
from utils.openai_client import generate_anki_fields
from utils.tts_client import generate_audio_files

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)  # type: ignore[misc]
def get_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)  # type: ignore[misc]
def generate_card(request: Request, word: Annotated[str, Form(...)]) -> HTMLResponse:
    fields = generate_anki_fields(word)
    image_url = fetch_image_url(word)
    audio_word, audio_sentence = generate_audio_files(fields)

    fields["Image"] = image_url
    fields["AudioWord"] = audio_word
    fields["AudioSentence"] = audio_sentence

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "preview": fields},
    )


@app.post("/submit", response_class=HTMLResponse)  # type: ignore[misc]
def submit_card(request: Request, word: Annotated[str, Form(...)]) -> HTMLResponse:
    fields = generate_anki_fields(word)
    fields["Image"] = fetch_image_url(word)
    fields["AudioWord"], fields["AudioSentence"] = generate_audio_files(fields)
    send_to_ankiweb(fields)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "confirmation": True},
    )
