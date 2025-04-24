def generate_audio_files(fields: dict[str, str]) -> tuple[str, str]:
    word_audio = f"/static/audio/{fields['Word']}_word.mp3"
    sentence_audio = f"/static/audio/{fields['Word']}_sentence.mp3"
    return word_audio, sentence_audio
