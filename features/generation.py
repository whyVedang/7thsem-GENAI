import streamlit as st

import config


PROMPT = r'''You are an intelligent AI programming assistant developed by IBM. Your primary function
is to assist users in code generation. With whatever prompt the user inputs, you have to
generate the full working code only. No extra texts at the starting and the beginning.

Examples for u to understand:

Input 1: Develop an optimized, bug-free Python function to detect strobogrammatic numbers.
Output 1:
def is_strobogrammatic(num: str) -> bool:
    # Define valid strobogrammatic digit mappings
    valid_map = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}

    # Check from both ends towards the center
    left, right = 0, len(num) - 1
    while left <= right:
        if num[left] not in valid_map or num[right] not in valid_map:
            return False
        if valid_map[num[left]] != num[right]:
            return False
        left += 1
        right -= 1

    return True'''


def render():
    st.title("Code Wizard")
    st.write("Generate code in any programming language based on your text input.")

    prompt = st.text_area("Enter your prompt:", placeholder="e.g., Create a function to add two numbers in Python")

    if not st.button("Generate Code"):
        return
    if not prompt.strip():
        st.warning("Please enter a prompt.")
        return

    config.require_provider("ibm")
    with st.spinner("Generating code with IBM Granite..."):
        try:
            code, model_used = config.generate_code(
                f"{PROMPT}\n\nTask: {prompt}", extract_code=True
            )
            st.code(code)
            st.caption(f"Generated using {model_used}")
        except Exception as e:
            st.error(f"Error generating code: {e}")
