import streamlit as st

from features.pair_programming import render


st.set_page_config(page_title="AI Pair Coder · ISL75", layout="wide")
st.caption("Course code ISL75 · Intelligent Code Generation and Code Explanation Assistant")
render()
