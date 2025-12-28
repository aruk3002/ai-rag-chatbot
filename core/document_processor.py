"""
Document Processing Utilities
=============================
This module handles preparing raw documents for downstream
embedding and retrieval.

Responsibilities:
- Load supported document formats (PDF, TXT)
- Normalize input into LangChain Document objects
- Split content into retrievable chunks
"""

from typing import List
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings


class DocumentProcessor:
    """
    Prepares documents for vector indexing by loading
    and chunking them into manageable pieces.
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ):
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

        self._splitter = self._init_splitter()

    def _init_splitter(self) -> RecursiveCharacterTextSplitter:
        """
        Initialize the text splitter with a consistent
        hierarchy of separators.
        """
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

    # -------------------------
    # Loading helpers
    # -------------------------

    def _load_from_file(self, file_path: str) -> List[Document]:
        """
        Load a document from disk based on file extension.
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == ".txt":
            loader = TextLoader(file_path, encoding="utf-8")
        elif suffix == ".pdf":
            loader = PyPDFLoader(file_path)
        else:
            raise ValueError(
                f"Unsupported file format: {suffix}. Only .txt and .pdf are allowed."
            )

        return loader.load()

    def _load_from_string(
        self, text: str, metadata: dict | None = None
    ) -> List[Document]:
        """
        Wrap raw text input into a Document object.
        """
        return [Document(page_content=text, metadata=metadata or {})]

    # -------------------------
    # Public API
    # -------------------------

    def split(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into overlapping chunks.
        """
        return self._splitter.split_documents(documents)

    def process_file(self, file_path: str) -> List[Document]:
        """
        Full pipeline for file-based documents:
        load → split → return chunks.
        """
        documents = self._load_from_file(file_path)
        return self.split(documents)

    def process_text(
        self, text: str, metadata: dict | None = None
    ) -> List[Document]:
        """
        Full pipeline for raw text input.
        """
        documents = self._load_from_string(text, metadata)
        return self.split(documents)
