import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_anki_fields(word: str) -> dict[str, str]:
    prompt = f"""
    For the Spanish word '{word}', create the following fields for an Anki card:
    - Word
    - Cloze Sentence (in Spanish, with the word replaced as {{c1::word}})
    - Full Sentence (in Spanish)
    - Translation (of the sentence in English)
    - Grammar Notes (short explanation of grammar)
    """
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    content = response.choices[0].message.content
    result = {}
    if content:
        lines = content.splitlines()
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                result[key.strip()] = value.strip()
    return result
