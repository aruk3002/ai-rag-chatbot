# 🧠 AI RAG Chatbot

### Multi-Document Retrieval-Augmented Generation with Optional Real-Time Web Search

<img width="1864" height="921" alt="Screenshot 2025-12-28 161716" src="https://github.com/user-attachments/assets/49bfa6c5-38e4-4249-b3df-fff7dd678fb9" />


---

## 📌 Overview

The **AI RAG Chatbot** is a Streamlit-based intelligent assistant that enables users to ask natural-language questions across their own documents using **Retrieval-Augmented Generation (RAG)**.
The system combines **local semantic search** over uploaded documents with **optional real-time web search**, ensuring responses are both **grounded** and **up-to-date**.

This project demonstrates a production-style hybrid RAG architecture using modern LLM tooling and clean software design principles.

---

## 🚀 Key Features

* 📄 **Multi-Document Question Answering**
  Query multiple uploaded PDF and TXT documents simultaneously.

* 🔍 **Semantic Search with FAISS**
  High-performance vector similarity search over embedded document chunks.

* 🌐 **Optional Real-Time Web Search**
  Augment document answers with live web results using Tavily.

* 📚 **Source-Aware Responses**
  Answers include transparent citations from documents and/or web sources.

* 💬 **Streaming Chat Interface**
  Token-level response streaming for a smooth conversational experience.

* 🧩 **Modular & Maintainable Architecture**
  Clear separation of concerns across ingestion, retrieval, generation, and UI.

---

## 🏗️ Architecture Overview

The system follows a **hybrid RAG pipeline**:

1. **Document Ingestion**

   * User uploads PDF/TXT files
   * Documents are cleaned, chunked, and normalized
   * Metadata is preserved for traceability

2. **Embedding & Indexing**

   * Text chunks are converted to embeddings using HuggingFace models
   * FAISS is used as a local vector database

3. **Query Processing**

   * User query triggers semantic retrieval from FAISS
   * Optional web search is executed for real-time augmentation

4. **Context Assembly**

   * Retrieved document chunks and web snippets are combined
   * Context is injected into the LLM prompt

5. **Answer Generation**

   * Groq-hosted LLM generates grounded responses
   * Streaming output is rendered in the UI

---

## 🛠️ Technology Stack

| Component     | Technology                        |
| ------------- | --------------------------------- |
| Language      | Python                            |
| LLM           | Groq (ChatGroq)                   |
| Embeddings    | HuggingFace Sentence Transformers |
| Vector Store  | FAISS                             |
| Web Search    | Tavily                            |
| UI            | Streamlit                         |
| Orchestration | LangChain                         |

---

## 📂 Project Structure

```
.
├── app.py                     # Streamlit entry point
├── config/
│   └── settings.py            # Centralized configuration & secrets
├── core/
│   ├── document_processor.py  # Document loading & chunking
│   ├── embeddings.py          # Embedding generation
│   ├── vector_store.py        # FAISS index management
│   └── chain.py               # RAG orchestration
├── tools/
│   └── tavily_search.py       # Web search integration
├── ui/
│   ├── components.py          # Reusable UI components
│   └── chat_interface.py      # Chat orchestration logic
├── data/
│   ├── documents/             # Uploaded documents
│   └── faiss_index/           # Persisted FAISS index
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone <your-github-repo-url>
cd <project-folder>
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```
---

## 🧪 Example Use Cases

* Ask conceptual questions from research papers or notes
* Combine internal documents with live web information
* Perform transparent, citation-aware knowledge retrieval
* Build a foundation for enterprise knowledge assistants

---

## 🔍 Evaluation Highlights

* Accurate retrieval of relevant document chunks
* Clear separation between document-based and web-based answers
* Consistent source attribution
* Stable performance with multiple documents

---

## 🔮 Future Enhancements

* Query intent classification (document vs web vs hybrid)
* Session-level memory and chat history persistence
* Support for additional document formats
* User-selectable LLM models
* Deployment on Streamlit Cloud or Docker

