"""
Vector Index Management
=======================
This module manages all interactions with the FAISS vector index.

Responsibilities:
- Create and update a FAISS index
- Perform similarity searches
- Persist and reload the index from disk
"""

import os
from typing import List, Optional, Tuple

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from config.settings import settings
from core.embeddings import EmbeddingManager


class VectorStoreManager:
    """
    Wrapper around FAISS that provides a clean interface
    for indexing, searching, and persistence.
    """

    def __init__(self, embedding_manager: EmbeddingManager | None = None):
        self.embedding_manager = embedding_manager or EmbeddingManager()
        self._index: Optional[FAISS] = None
        self._index_path = settings.FAISS_INDEX_PATH

    # -------------------------
    # State helpers
    # -------------------------

    @property
    def is_initialized(self) -> bool:
        """Return True if an index is currently loaded in memory."""
        return self._index is not None

    @property
    def vector_store(self) -> Optional[FAISS]:
        """Expose the raw FAISS object when needed."""
        return self._index

    # -------------------------
    # Index creation & updates
    # -------------------------

    def _build_index(self, documents: List[Document]) -> FAISS:
        """
        Create a new FAISS index from documents.
        """
        self._index = FAISS.from_documents(
            documents=documents,
            embedding=self.embedding_manager.embeddings,
        )
        return self._index

    def upsert(self, documents: List[Document]) -> None:
        """
        Add documents to the index. If the index does not
        exist yet, it will be created automatically.
        """
        if not self.is_initialized:
            self._build_index(documents)
        else:
            self._index.add_documents(documents)

    # -------------------------
    # Search operations
    # -------------------------

    def search(self, query: str, k: int | None = None) -> List[Document]:
        """
        Perform similarity search against the index.
        """
        if not self.is_initialized:
            raise ValueError("Vector index is not initialized.")

        k = k or settings.TOP_K_RESULTS
        return self._index.similarity_search(query, k=k)

    def search_with_scores(
        self, query: str, k: int | None = None
    ) -> List[Tuple[Document, float]]:
        """
        Perform similarity search and return relevance scores.
        """
        if not self.is_initialized:
            raise ValueError("Vector index is not initialized.")

        k = k or settings.TOP_K_RESULTS
        return self._index.similarity_search_with_score(query, k=k)

    def as_retriever(self, k: int | None = None):
        """
        Return a LangChain-compatible retriever interface.
        """
        if not self.is_initialized:
            raise ValueError("Vector index is not initialized.")

        k = k or settings.TOP_K_RESULTS
        return self._index.as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )

    # -------------------------
    # Persistence
    # -------------------------

    def save(self, path: str | None = None) -> None:
        """
        Persist the current index to disk.
        """
        if not self.is_initialized:
            raise ValueError("No vector index to save.")

        save_path = path or self._index_path
        os.makedirs(save_path, exist_ok=True)
        self._index.save_local(save_path)

    def load(self, path: str | None = None) -> FAISS:
        """
        Load an index from disk into memory.
        """
        load_path = path or self._index_path

        if not os.path.exists(load_path):
            raise FileNotFoundError(f"FAISS index not found at: {load_path}")

        self._index = FAISS.load_local(
            load_path,
            self.embedding_manager.embeddings,
            allow_dangerous_deserialization=True,
        )
        return self._index

    def clear(self) -> None:
        """
        Remove the in-memory index.
        """
        self._index = None
