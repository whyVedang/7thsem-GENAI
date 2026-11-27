import streamlit as st

import config


PROMPT = "Review the following code and provide suggestions for improvements or fixes:"


def render():
    st.title("AI Pair Coder")
    st.write(
        "Write your code below, and the AI will provide real-time suggestions and improvements as you type."
    )

    if "pair_programming_code" not in st.session_state:
        st.session_state.pair_programming_code = ""

    code = st.text_area(
        "Write your code here:",
        height=400,
        placeholder="Start typing your code...",
        key="pair_programming_code",
    )

    if not code.strip():
        st.warning("Please start typing your code to get AI suggestions.")
        return

    config.require_provider("ibm")
    with st.spinner("IBM Granite is analyzing your code..."):
        try:
            suggestions, model_used = config.generate_code(f"{PROMPT}\n{code}")
            st.subheader("AI Suggestions:")
            st.markdown(suggestions)
            st.caption(f"Analyzed using {model_used}")
        except Exception as error:
            st.error(f"Error getting suggestions: {error}")
