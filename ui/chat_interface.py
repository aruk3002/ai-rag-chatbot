"""
Chat Runtime Controller
=======================
Coordinates document ingestion, retrieval,
and response generation for the chat interface.
"""

from typing import Generator, Optional, List

import streamlit as st

from core.document_processor import DocumentProcessor
from core.vector_store import VectorStoreManager
from core.chain import RAGChain
from tools.tavily_search import TavilyWebSearch, HybridSearchService
from ui.components import persist_uploaded_file


class ChatController:
    """
    High-level controller responsible for handling
    user queries and managing retrieval strategies.
    """

    def __init__(self):
        self._doc_processor = DocumentProcessor()
        self._vector_store = VectorStoreManager()

        self._rag_chain: Optional[RAGChain] = None
        self._web_search = TavilyWebSearch()
        self._hybrid_search: Optional[HybridSearchService] = None

    # -------------------------
    # Document ingestion
    # -------------------------

    def ingest_files(self, uploaded_files) -> int:
        """
        Process uploaded files and index their content.
        """
        collected_chunks = []

        for uploaded_file in uploaded_files:
            file_path = persist_uploaded_file(uploaded_file)
            chunks = self._doc_processor.process_file(file_path)

            for chunk in chunks:
                chunk.metadata["source"] = uploaded_file.name

            collected_chunks.extend(chunks)

            if uploaded_file.name not in st.session_state.uploaded_files:
                st.session_state.uploaded_files.append(uploaded_file.name)

        if collected_chunks:
            self._vector_store.upsert(collected_chunks)
            st.session_state.vector_ready = True

        return len(collected_chunks)

    # -------------------------
    # Initialization helpers
    # -------------------------

    def _ensure_rag_ready(self):
        """
        Initialize RAG components lazily after documents are indexed.
        """
        if self._vector_store.is_initialized and self._rag_chain is None:
            self._rag_chain = RAGChain(self._vector_store)
            self._hybrid_search = HybridSearchService(
                self._vector_store, self._web_search
            )

    # -------------------------
    # Query handling
    # -------------------------

    def stream_answer(
        self, question: str, include_web: bool = False
    ) -> Generator[str, None, None]:
        """
        Stream an answer for a user query.
        """
        self._ensure_rag_ready()

        if not self._vector_store.is_initialized and not include_web:
            yield "Please upload documents or enable web search to continue."
            return

        if include_web:
            yield from self._stream_hybrid_answer(question)
        else:
            yield from self._stream_document_answer(question)

    def _stream_document_answer(self, question: str) -> Generator[str, None, None]:
        """
        Stream an answer using document-only RAG.
        """
        if not self._rag_chain:
            yield "No indexed documents available."
            return

        for chunk in self._rag_chain.query_stream(question):
            yield chunk

    def _stream_hybrid_answer(self, question: str) -> Generator[str, None, None]:
        """
        Stream an answer using both documents and web search.
        """
        search_results = self._hybrid_search.search(
            query=question,
            include_web=True,
        )

        context = self._hybrid_search.build_context(
            documents=search_results["documents"],
            web_text=search_results["web"],
        )

        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from config.settings import settings

        llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            api_key=settings.GROQ_API_KEY,
        )

        prompt = ChatPromptTemplate.from_template(
            "Answer the question using the context below.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )

        chain = prompt | llm

        for token in chain.stream(
            {"context": context, "question": question}
        ):
            yield token.content

    # -------------------------
    # Source extraction
    # -------------------------

    def collect_sources(
        self, question: str, include_web: bool = False
    ) -> List[str]:
        """
        Collect source labels for a given query.
        """
        sources = set()

        if self._vector_store.is_initialized:
            docs = self._vector_store.search(question)
            for doc in docs:
                sources.add(doc.metadata.get("source", "Unknown"))

        if include_web:
            sources.add("Web Search")

        return list(sources)
