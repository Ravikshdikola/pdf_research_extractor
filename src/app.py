import streamlit as st
from pipeline import run_pipeline
import os

# Set output folder relative to project root
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.title("PDF Research Paper Extractor")

st.markdown("""
Upload a research paper PDF, and this app will extract the DOI, ISSN, title, authors, and a brief summary using OCR and LLM-powered RAG.
""")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_pdf_path = os.path.join("temp_uploaded.pdf")
    with open(temp_pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.info(f"Uploaded file saved to {temp_pdf_path}")

    # Output Excel path
    output_excel_path = os.path.join(OUTPUT_DIR, "extracted_data.xlsx")

    try:
        with st.spinner("Running extraction pipeline... This might take a few minutes."):
            run_pipeline(temp_pdf_path, output_excel_path)

        st.success("Extraction completed!")
        st.markdown(f"Output saved to `{output_excel_path}`")

        # Optionally, read and display extracted info in the app
        import pandas as pd
        df = pd.read_excel(output_excel_path, engine='openpyxl')
        st.dataframe(df)

    except Exception as e:
        st.error(f"An error occurred: {e}")

    # Cleanup temp PDF if needed
    # os.remove(temp_pdf_path)
else:
    st.info("Please upload a PDF file to start.")
