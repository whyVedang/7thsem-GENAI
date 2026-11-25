from importlib import import_module
from importlib.util import find_spec

import streamlit as st

# The launcher owns the display order. Missing modules stay off the menu.
FEATURES = (
    ("Code Wizard", "features.generation"),
    ("Fix-It", "features.debugging"),
    ("Code Whisperer", "features.explanations"),
    ("Code Optimizer", "features.refactoring"),
    ("DocuBot", "features.documents"),
    ("AI Pair Coder", "features.pair_programming"),
)

st.set_page_config(page_title="GenAI Project · ISL75", layout="wide")
st.title("GenAI Project")
st.caption("Course code ISL75 · Intelligent Code Generation and Code Explanation Assistant")

available = {label: module for label, module in FEATURES if find_spec(module) is not None}
st.sidebar.title("Navigation")
page = st.sidebar.radio("Page", ["Home", *available])

if page == "Home":
    st.header("Home")
    st.write("Generate code from a natural-language request or explore what existing code does.")
    if available:
        st.write("Choose a tool from the sidebar.")
    else:
        st.write("The Home page is ready. Tools will appear as their modules are added.")
else:
    import_module(available[page]).render()
