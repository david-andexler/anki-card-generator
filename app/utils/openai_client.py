import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_anki_fields(
    input_word_or_phrase: str,
    target_language: str,
    translation_language: str,
) -> dict[str, str]:
    prompt = f"""
    For the {target_language} word '{input_word_or_phrase}', create the "
    "following fields for an Anki card:
    - Word
    - Cloze Sentence (in {target_language}, with the word replaced as {{c1::word}})
    - Full Sentence (in {target_language})
    - Translation (of the sentence in {translation_language})
    - Grammar Notes (short explanation of grammar in {translation_language})
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
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
