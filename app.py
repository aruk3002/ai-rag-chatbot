"""
RAG Chat Application
===================
Streamlit entry point for the document-based
Retrieval-Augmented Generation chatbot.
"""

import streamlit as st

from config.settings import settings
from ui.components import (
    initialize_session,
    render_chat_messages,
    append_message,
    render_sidebar,
    file_uploader,
    show_status,
    web_search_toggle,
)
from ui.chat_interface import ChatController


# -------------------------
# App configuration
# -------------------------

st.set_page_config(
    page_title="Chat Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        /* Main container spacing */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 1200px;
        }

        /* Sidebar container */
        section[data-testid="stSidebar"] {
            padding-top: 0.5rem;
        }

        /* Sidebar inner content spacing */
        section[data-testid="stSidebar"] > div {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* Reduce vertical gaps inside sidebar */
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {
            margin-top: 0.5rem;
            margin-bottom: 0.25rem;
        }

        section[data-testid="stSidebar"] hr {
            margin: 0.75rem 0;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] li {
            margin-bottom: 0.35rem;
        }

        /* Prevent unnecessary sidebar scroll */
        section[data-testid="stSidebar"] {
            overflow: hidden;
        }

        /* Chat input polish */
        textarea[data-testid="stChatInputTextarea"] {
            border-radius: 24px;
            padding: 0.75rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



# -------------------------
# Startup validation
# -------------------------

try:
    settings.validate()
except ValueError as err:
    st.error(f"Configuration error:\n\n{err}")
    st.stop()


# -------------------------
# Application bootstrap
# -------------------------

def bootstrap():
    """
    Initialize session state and controller instances.
    """
    initialize_session()

    if "chat_controller" not in st.session_state:
        st.session_state.chat_controller = ChatController()


def main():
    bootstrap()
    controller: ChatController = st.session_state.chat_controller

    # Sidebar
    render_sidebar()

    # Header
    st.title("🤖 AI Chatbot")
    st.caption("Ask questions across your documents with optional web search")

    # -------------------------
    # Document upload section
    # -------------------------

    with st.expander(
        "Upload documents",
        expanded=not st.session_state.vector_ready,
    ):
        uploaded_files = file_uploader()

        if uploaded_files and st.button("Index documents", type="primary"):
            with st.spinner("Indexing documents..."):
                try:
                    chunks = controller.ingest_files(uploaded_files)
                    show_status(
                        f"Indexed {len(uploaded_files)} file(s) into {chunks} chunks",
                        level="success",
                    )
                except Exception as exc:
                    show_status(str(exc), level="error")

    # -------------------------
    # Controls
    # -------------------------

    include_web = web_search_toggle()
    st.divider()

    # -------------------------
    # Chat history
    # -------------------------

    render_chat_messages()

    # -------------------------
    # Chat input
    # -------------------------

    user_input = st.chat_input("Ask a question...")
    if user_input:
        # Render user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)

        append_message("user", user_input)

        # Render assistant response
        with st.chat_message("assistant"):
            try:
                response = st.write_stream(
                    controller.stream_answer(
                        question=user_input,
                        include_web=include_web,
                    )
                )

                sources = controller.collect_sources(
                    question=user_input,
                    include_web=include_web,
                )

                if sources:
                    with st.expander("Sources"):
                        for src in sources:
                            st.write(f"- {src}")

                append_message("assistant", response, sources)

            except Exception as exc:
                error_text = f"Error generating response: {exc}"
                st.error(error_text)
                append_message("assistant", error_text)


if __name__ == "__main__":
    main()
