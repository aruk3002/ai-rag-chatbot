"""
Streamlit UI Utilities
=====================
Reusable UI helpers for managing chat state,
file uploads, and sidebar layout.
"""

import os
import tempfile
from typing import List, Optional

import streamlit as st


# -------------------------
# Session state helpers
# -------------------------

def initialize_session():
    """
    Initialize all required Streamlit session variables.
    """
    st.session_state.setdefault("chat_messages", [])
    st.session_state.setdefault("vector_ready", False)
    st.session_state.setdefault("uploaded_files", [])


# -------------------------
# Chat helpers
# -------------------------

def render_chat_messages():
    """
    Render chat history from session state.
    """
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("Sources"):
                    for src in message["sources"]:
                        st.write(f"- {src}")


def append_message(
    role: str,
    content: str,
    sources: Optional[List[str]] = None,
):
    """
    Append a message to the chat history.
    """
    entry = {"role": role, "content": content}
    if sources:
        entry["sources"] = sources

    st.session_state.chat_messages.append(entry)


def reset_chat():
    """
    Clear all chat messages.
    """
    st.session_state.chat_messages = []


# -------------------------
# File upload helpers
# -------------------------

def persist_uploaded_file(uploaded_file) -> str:
    """
    Save an uploaded file to a temporary directory and
    return its local path.
    """
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def file_uploader():
    """
    Display the document upload widget.
    """
    return st.file_uploader(
        label="Upload documents (PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Uploaded documents will be indexed for retrieval",
    )


# -------------------------
# Sidebar layout
# -------------------------

def render_sidebar():
    with st.sidebar:
        st.markdown("### 🤖 AI RAG Chatbot")
        st.caption(
            "Query your documents with optional real-time web search."
        )

        st.divider()

        st.markdown("#### Capabilities")
        st.markdown(
            """
            • 📄 PDF / TXT document Q&A  
            • 🔍 Optional web augmentation  
            • 📚 Source-aware answers  
            """
        )

        st.divider()

        st.markdown("#### 📁 Documents")
        if st.session_state.uploaded_files:
            for i, name in enumerate(st.session_state.uploaded_files, 1):
                st.markdown(f"{i}. {name}")
        else:
            st.caption("No documents uploaded")

        st.divider()

        if st.button("🗑️ Clear conversation", use_container_width=True):
            reset_chat()
            st.rerun()

        # Footer (subtle, professional)
        st.caption("Built with Streamlit · RAG · FAISS")



# -------------------------
# Status & controls
# -------------------------

def show_status(message: str, level: str = "info"):
    """
    Display a status message.
    """
    if level == "success":
        st.success(message)
    elif level == "warning":
        st.warning(message)
    elif level == "error":
        st.error(message)
    else:
        st.info(message)


def web_search_toggle() -> bool:
    """
    Toggle for enabling/disabling web search.
    """
    return st.toggle(
        "Enable web search",
        value=False,
        help="Include live web results when answering questions",
    )
