"""
Embedding Utilities
===================
This module provides a thin wrapper around HuggingFace
sentence-transformer models for generating text embeddings.
"""

from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import settings


class EmbeddingManager:
    """
    Handles creation of vector embeddings for text inputs.
    """

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL

        self._model = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        """Expose the underlying embedding model."""
        return self._model

    def embed(self, text: str) -> List[float]:
        """
        Generate an embedding for a single text input.
        """
        return self._model.embed_query(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple text inputs.
        """
        return self._model.embed_documents(texts)

    def dimension(self) -> int:
        """
        Return the embedding vector size.
        """
        return len(self.embed("dimension_check"))
