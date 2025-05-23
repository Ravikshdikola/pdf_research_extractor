import re
import logging

def extract_metadata(text: str) -> dict:
    """Extract DOI and ISSN from text using regex."""
    try:
        doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text, re.I)
        issn_match = re.search(r"ISSN[:\s]*\d{4}-\d{3}[\dX]", text, re.I)
        return {
            "DOI": doi_match.group(0) if doi_match else "Not found",
            "ISSN": issn_match.group(0) if issn_match else "Not found"
        }
    except Exception as e:
        logging.error(f"Error extracting metadata: {e}")
        return {"DOI": "Error", "ISSN": "Error"}
