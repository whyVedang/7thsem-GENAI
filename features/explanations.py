import streamlit as st

import config
from features import audio


PROMPT = (
    "Analyze and explain the following code clearly for a beginner. "
    "Describe its purpose, important steps, and any notable behavior."
)


def _explanation_prompt(code):
    return f"{PROMPT}\n\nCode:\n{code}"


def render():
    st.title("Code Whisperer")
    st.write("Get a detailed explanation of your code as text or audio.")

    code = st.text_area("Enter your code:", placeholder="Paste your code here")

    if st.button("Generate Text Explanation"):
        if not code.strip():
            st.warning("Please enter some code to explain.")
            return

        config.require_provider("ibm")
        with st.spinner("Explaining code with IBM Granite..."):
            try:
                explanation, model_used = config.generate_code(
                    _explanation_prompt(code)
                )
                st.text_area("Explanation:", value=explanation, height=300)
                st.caption(f"Explained using {model_used}")
            except Exception as error:
                st.error(f"Error explaining code: {error}")

    if st.button("Generate Audio Explanation"):
        if not code.strip():
            st.warning("Please enter some code before generating an explanation.")
            return

        config.require_provider("ibm")
        with st.spinner("Generating audio explanation..."):
            try:
                explanation, model_used = config.generate_code(
                    _explanation_prompt(code)
                )
                audio_data = audio.text_to_speech(explanation)
                st.subheader("Generated Audio Explanation:")
                st.audio(audio_data, format="audio/mp3")
                st.download_button(
                    label="Download as MP3",
                    data=audio_data,
                    file_name="explanation.mp3",
                    mime="audio/mp3",
                )
                st.caption(f"Explained using {model_used}")
            except Exception as error:
                st.error(f"Error generating audio explanation: {error}")
