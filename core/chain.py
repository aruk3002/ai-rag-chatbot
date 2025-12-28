"""
RAG Execution Layer
===================
This module is responsible for running the end-to-end
Retrieval-Augmented Generation (RAG) workflow.

Role of this file:
- Accept user queries
- Fetch relevant document chunks from FAISS
- Inject context into the prompt
- Generate grounded answers using Groq LLM

This file intentionally does NOT handle:
- Document ingestion
- Embeddings creation
- Vector indexing
"""

from typing import List, Generator, Dict
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from config.settings import settings
from core.vector_store import VectorStoreManager


# Prompt used for document-grounded answering
QA_PROMPT = """
You are an AI assistant answering questions using the provided context.
If the context does not contain enough information, say so clearly.

Context:
{context}

Question:
{question}

Answer:
"""


class RAGChain:
    """
    Central coordinator for the RAG workflow.

    High-level steps:
    1. Retrieve relevant chunks from vector store
    2. Build a context string
    3. Generate an answer using the LLM
    """

    def __init__(
        self,
        vector_store: VectorStoreManager,
        model_name: str | None = None,
        temperature: float | None = None,
    ):
        self.vector_store = vector_store

        self.model_name = model_name or settings.LLM_MODEL
        self.temperature = (
            temperature if temperature is not None else settings.LLM_TEMPERATURE
        )

        # Initialize Groq chat model
        self._model = ChatGroq(
            model=self.model_name,
            temperature=self.temperature,
            api_key=settings.GROQ_API_KEY,
        )

        # Prompt + output parser
        self._qa_prompt = ChatPromptTemplate.from_template(QA_PROMPT)
        self._parser = StrOutputParser()

    @property
    def llm(self) -> ChatGroq:
        """Expose the underlying LLM instance if needed."""
        return self._model

    # -------------------------
    # Internal helper methods
    # -------------------------

    def _fetch_documents(self, query: str, k: int | None = None) -> List[Document]:
        """
        Fetch top-k relevant documents from the vector store.
        """
        if not self.vector_store.is_initialized:
            return []

        return self.vector_store.search(query, k=k)

    def _build_context(self, docs: List[Document]) -> str:
        """
        Convert retrieved documents into a single context string
        that can be injected into the prompt.
        """
        if not docs:
            return "No relevant context found."

        blocks = []
        for idx, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "Unknown")
            blocks.append(
                f"[Document {idx}] (Source: {source})\n{doc.page_content}"
            )

        return "\n\n".join(blocks)

    def _run_generation(self, question: str, context: str) -> str:
        """
        Run the prompt → LLM → parser pipeline.
        """
        chain = self._qa_prompt | self._model | self._parser
        return chain.invoke({"question": question, "context": context})

    def _run_generation_stream(
        self, question: str, context: str
    ) -> Generator[str, None, None]:
        """
        Streaming version of answer generation.
        """
        chain = self._qa_prompt | self._model | self._parser
        for chunk in chain.stream({"question": question, "context": context}):
            yield chunk

    # -------------------------
    # Public API
    # -------------------------

    def query(self, question: str, k: int | None = None) -> Dict:
        """
        Execute the full RAG pipeline for a single query.
        """
        documents = self._fetch_documents(question, k)
        context = self._build_context(documents)
        answer = self._run_generation(question, context)

        sources = list(
            {doc.metadata.get("source", "Unknown") for doc in documents}
        )

        return {
            "answer": answer,
            "sources": sources,
            "context": context,
            "documents": documents,
        }

    def query_stream(
        self, question: str, k: int | None = None
    ) -> Generator[str, None, None]:
        """
        Execute the RAG pipeline with token streaming.
        """
        documents = self._fetch_documents(question, k)
        context = self._build_context(documents)

        for chunk in self._run_generation_stream(question, context):
            yield chunk
