import numpy as np
from langchain.embeddings import OllamaEmbeddings

class WrappedOllamaEmbeddings(OllamaEmbeddings):
    """
    Wrapper to convert Ollama embedding outputs to numpy float32 arrays.
    """
    def embed_query(self, text: str) -> np.ndarray:
        vec = super().embed_query(text)
        return np.array(vec, dtype=np.float32)

    def embed_documents(self, texts: list[str]) -> list[np.ndarray]:
        vecs = super().embed_documents(texts)
        return [np.array(v, dtype=np.float32) for v in vecs]
