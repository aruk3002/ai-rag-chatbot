"""
Web Search Utilities (Tavily)
=============================
This module provides optional real-time web search
capabilities using the Tavily API.

It is designed to complement local document retrieval
when queries require up-to-date or external information.
"""

import os
from typing import List, Optional, Literal

from langchain_tavily import TavilySearch

from config.settings import settings


class TavilyWebSearch:
    """
    Lightweight wrapper around the Tavily search API.
    """

    def __init__(
        self,
        max_results: int = 3,
        topic: Literal["general", "news", "finance"] = "general",
    ):
        self.max_results = max_results
        self.topic = topic

        # Tavily expects the API key to be available as an env variable
        os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

        self._client = TavilySearch(
            max_results=self.max_results,
            topic=self.topic,
        )

    def run(self, query: str) -> str:
        """
        Execute a web search and return a readable text block.
        """
        raw_results = self._client.invoke(query)
        return self._format(raw_results)

    def run_structured(self, query: str) -> dict:
        """
        Execute a web search and return both raw and formatted output.
        """
        raw_results = self._client.invoke(query)

        return {
            "query": query,
            "source": "tavily_web_search",
            "raw": raw_results,
            "formatted": self._format(raw_results),
        }

    def _format(self, results: dict) -> str:
        """
        Convert Tavily output into a context-friendly string.
        """
        if not results:
            return "No web search results available."

        sections = []

        if results.get("answer"):
            sections.append(f"Summary:\n{results['answer']}")

        if results.get("results"):
            for idx, item in enumerate(results["results"], start=1):
                title = item.get("title", "Untitled")
                content = item.get("content", "")
                url = item.get("url", "")
                sections.append(
                    f"[Web {idx}] {title}\n{content}\nSource: {url}"
                )

        return "\n\n".join(sections) if sections else "No relevant web content found."


class HybridSearchService:
    """
    Combines local document search with optional web search.
    """

    def __init__(self, vector_store, web_search: TavilyWebSearch | None = None):
        self.vector_store = vector_store
        self.web_search = web_search or TavilyWebSearch()

    def search(
        self,
        query: str,
        include_web: bool = False,
        doc_k: int = 3,
    ) -> dict:
        """
        Run document search and optionally augment with web results.
        """
        response = {
            "query": query,
            "documents": [],
            "web": None,
        }

        if self.vector_store.is_initialized:
            response["documents"] = self.vector_store.search(query, k=doc_k)

        if include_web:
            response["web"] = self.web_search.run(query)

        return response

    def build_context(
        self,
        documents: List,
        web_text: Optional[str] = None,
    ) -> str:
        """
        Assemble a single context string from multiple sources.
        """
        context_blocks = []

        if documents:
            context_blocks.append("=== Document Context ===")
            for idx, doc in enumerate(documents, start=1):
                source = doc.metadata.get("source", "Unknown")
                context_blocks.append(
                    f"[Doc {idx}] ({source})\n{doc.page_content}"
                )

        if web_text:
            context_blocks.append("\n=== Web Context ===")
            context_blocks.append(web_text)

        return "\n\n".join(context_blocks) if context_blocks else "No context available."
