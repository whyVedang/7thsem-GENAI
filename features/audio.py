import io
import json

import config


def text_to_speech(text):
    """Convert explanation text to MP3 bytes, using Google Cloud when configured."""
    credentials_json = config.secret("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    credentials_path = config.secret("GOOGLE_APPLICATION_CREDENTIALS")

    if credentials_json or credentials_path:
        from google.cloud import texttospeech
        from google.oauth2 import service_account

        if credentials_json:
            credentials_info = json.loads(credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info
            )
        else:
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )

        client = texttospeech.TextToSpeechClient(credentials=credentials)
        response = client.synthesize_speech(
            input=texttospeech.SynthesisInput(text=text),
            voice=texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Chirp-HD-F",
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            ),
            audio_config=texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            ),
        )
        return response.audio_content

    from gtts import gTTS

    output = io.BytesIO()
    gTTS(text=text, lang="en").write_to_fp(output)
    return output.getvalue()
