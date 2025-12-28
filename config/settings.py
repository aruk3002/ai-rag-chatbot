"""
Application Configuration
=========================
Centralized configuration for the RAG application.

This module is responsible for:
- Loading environment variables
- Resolving secrets securely
- Exposing runtime configuration via a single settings object
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

# Disable tokenizer parallelism warnings (must be set early)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load .env for local development
load_dotenv()


def get_secret(key: str, default: Optional[str] = None) -> str:
    """
    Resolve secrets safely from multiple sources.

    Priority order:
    1. Streamlit secrets (if running in Streamlit)
    2. Environment variables
    3. Provided default
    """
    try:
        import streamlit as st

        secrets = getattr(st, "secrets", None)
        if secrets and key in secrets:
            return secrets[key]
    except Exception:
        # Streamlit may not be available or secrets may be missing
        pass

    return os.getenv(key, default or "")


@dataclass
class Settings:
    """
    Runtime configuration container.

    All values are loaded once at startup and reused
    throughout the application.
    """

    # -------------------------
    # API Keys
    # -------------------------
    GROQ_API_KEY: str = get_secret("GROQ_API_KEY", "")
    TAVILY_API_KEY: str = get_secret("TAVILY_API_KEY", "")

    # -------------------------
    # LLM configuration
    # -------------------------
    LLM_MODEL: str = "llama-3.1-8b-instant"
    LLM_TEMPERATURE: float = 0.5

    # -------------------------
    # Embeddings
    # -------------------------
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # -------------------------
    # Document processing
    # -------------------------
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # -------------------------
    # Vector store
    # -------------------------
    FAISS_INDEX_PATH: str = "data/faiss_index"

    # -------------------------
    # Retrieval
    # -------------------------
    TOP_K_RESULTS: int = 3

    def validate(self) -> bool:
        """
        Validate critical configuration values before runtime.
        """
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is missing. "
                "Set it using environment variables or Streamlit secrets."
            )

        if not self.TAVILY_API_KEY:
            raise ValueError(
                "TAVILY_API_KEY is missing. "
                "Set it using environment variables or Streamlit secrets."
            )

        if self.GROQ_API_KEY.startswith("your_") or len(self.GROQ_API_KEY) < 10:
            raise ValueError("Invalid GROQ_API_KEY detected.")

        if self.TAVILY_API_KEY.startswith("your_") or len(self.TAVILY_API_KEY) < 10:
            raise ValueError("Invalid TAVILY_API_KEY detected.")

        return True


# Shared configuration instance
settings = Settings()
