import streamlit as st

st.set_page_config(page_title="GenAI Project · ISL75", layout="wide")
st.title("GenAI Project")
st.caption("Course code ISL75 · Intelligent Code Generation and Code Explanation Assistant")

st.sidebar.title("Navigation")
st.sidebar.radio("Page", ["Home"])

st.header("Home")
st.write("A course project for generating code from natural-language requests and explaining existing code.")
