import logging
import pandas as pd
from langchain.llms import Ollama
from ocr import pdf_to_text
from metadata import extract_metadata
from rag import extract_rag_info

def save_to_excel(data: dict, output_path: str) -> None:
    """Save extracted data dictionary to Excel file."""
    try:
        df = pd.DataFrame([data])
        df.to_excel(output_path, index=False, engine='openpyxl')
    except Exception as e:
        logging.error(f"Failed to save output to Excel: {e}")
        raise

def run_pipeline(pdf_path: str, output_path: str) -> None:
    """
    Full pipeline:
    1. OCR extraction of PDF text
    2. Metadata extraction (DOI, ISSN)
    3. RAG info extraction (title, authors, summary)
    4. Save output to Excel
    """
    try:
        logging.info("Starting OCR extraction...")
        text = pdf_to_text(pdf_path)

        logging.info("Extracting DOI and ISSN metadata...")
        metadata = extract_metadata(text)

        logging.info("Initializing Ollama LLM model for RAG...")
        llm = Ollama(model="deepseek-r1:7b")

        logging.info("Extracting title, authors, summary using RAG...")
        rag_info = extract_rag_info(text, llm)

        combined_data = {**metadata, **rag_info}
        save_to_excel(combined_data, output_path)

        logging.info(f"Pipeline completed successfully. Output saved to {output_path}")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise
