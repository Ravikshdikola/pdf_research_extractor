from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms import Ollama
from embeddings import WrappedOllamaEmbeddings
from utils import extract_bracket_content
import logging

def extract_rag_info(text: str, llm: Ollama) -> dict:
    """
    Run Retrieval-Augmented Generation (RAG) using a local Ollama LLM model.
    Extracts title, authors, and summary enclosed in square brackets.
    """
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        texts = splitter.split_text(text)
        docs = [Document(page_content=t) for t in texts]

        embeddings = WrappedOllamaEmbeddings(model="nomic-embed-text")
        db = FAISS.from_documents(docs, embeddings)
        retriever = db.as_retriever()
        chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

        raw_title = chain.run("Return only the exact title of the paper as it appears in the document, enclosed inside square brackets [ ]. Do not add any extra text.")
        raw_authors = chain.run("Return only the list of authors exactly as shown in the document, enclosed inside square brackets [ ]. Do not add prefixes, suffixes, or explanations.")
        raw_summary = chain.run("Return only a 3-5 sentence summary of the paper’s content, enclosed inside square brackets [ ]. Do not include any introductory or closing phrases.")

        title = extract_bracket_content(raw_title) or raw_title.strip()
        authors = extract_bracket_content(raw_authors) or raw_authors.strip()
        summary = extract_bracket_content(raw_summary) or raw_summary.strip()

        return {
            "Title": title,
            "Authors": authors,
            "Summary": summary
        }
    except Exception as e:
        logging.error(f"Error during RAG extraction: {e}")
        return {"Title": "Error", "Authors": "Error", "Summary": "Error"}
