from typing import Any

import requests


def send_to_ankiweb(fields: dict[str, str]) -> Any:
    note = {
        "deckName": "Spanish Auto",
        "modelName": "Basic",
        "fields": {
            "Front": fields["Cloze Sentence"],
            "Back": f"{fields['Translation']}<br>{fields['Grammar Notes']}"
            f"<br>{fields['Full Sentence']}<br><img src='{fields['Image']}'>"
            f"<br>[sound:{fields['AudioSentence']}]",
        },
        "options": {"allowDuplicate": False, "duplicateScope": "deck"},
        "tags": ["auto"],
    }
    payload = {"action": "addNote", "version": 6, "params": {"note": note}}
    response = requests.post("http://localhost:8765", json=payload, timeout=10)
    response.raise_for_status()  # Raise an error for HTTP issues
    return response.json()
