import io
from xml.sax.saxutils import escape

import streamlit as st

import config


PROMPT = (
    "Write clear, structured documentation for the following code. "
    "Describe its purpose, inputs, outputs, and important implementation details."
)


def _pdf_bytes(documentation):
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import (
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )

    output = io.BytesIO()
    document = SimpleDocTemplate(output)
    body_style = getSampleStyleSheet()["BodyText"]
    content = []
    for line in documentation.splitlines():
        if line:
            content.append(Paragraph(escape(line), body_style))
        else:
            content.append(Spacer(1, body_style.leading))
    document.build(content)
    return output.getvalue()


def _show_exports(documentation):
    st.markdown("### Download Documentation")
    st.download_button(
        label="Download as TXT",
        data=documentation,
        file_name="documentation.txt",
        mime="text/plain",
    )

    try:
        from docx import Document

        docx_document = Document()
        docx_document.add_paragraph(documentation)
        docx_bytes = io.BytesIO()
        docx_document.save(docx_bytes)
        st.download_button(
            label="Download as DOCX",
            data=docx_bytes.getvalue(),
            file_name="documentation.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    except ImportError:
        st.warning("Install `python-docx` for DOCX export: `pip install python-docx`")

    try:
        pdf_data = _pdf_bytes(documentation)
        st.download_button(
            label="Download as PDF",
            data=pdf_data,
            file_name="documentation.pdf",
            mime="application/pdf",
        )
    except ImportError:
        st.warning("Install `reportlab` for PDF export: `pip install reportlab`")


def render():
    st.title("DocuBot")
    st.write("Generate documentation for your code automatically.")

    code = st.text_area("Enter your code:", placeholder="Paste your code here")

    if not st.button("Generate Document"):
        return
    if not code.strip():
        st.warning("Please enter some code to generate documentation.")
        return

    config.require_provider("ibm")
    with st.spinner("Generating documentation with IBM Granite..."):
        try:
            documentation, model_used = config.generate_code(
                f"{PROMPT}\n\nCode:\n{code}"
            )
            st.text_area("Documentation:", value=documentation, height=400)
            st.caption(f"Generated using {model_used}")
            _show_exports(documentation)
        except Exception as error:
            st.error(f"Error generating documentation: {error}")
