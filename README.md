# RAG Chatbot Workshop - 4 Day Course

A full-stack RAG (Retrieval-Augmented Generation) chatbot built with LangChain, Streamlit, FAISS, and Tavily search.

## 🎯 Course Overview

This project is designed for a **4-day workshop** (2 hours per day) teaching RAG application development.

### Day-by-Day Breakdown

| Day | Topic | Files | Key Concepts |
|-----|-------|-------|--------------|
| **Day 1** | Foundations & Document Processing | `config/`, `core/document_processor.py` | RAG intro, document loaders, text splitting |
| **Day 2** | Vector Store & Embeddings | `core/embeddings.py`, `core/vector_store.py` | Embeddings, FAISS, similarity search |
| **Day 3** | RAG Chain & Tavily Tool | `core/chain.py`, `tools/tavily_search.py` | LLM integration, chains, web search |
| **Day 4** | Streamlit UI & Integration | `ui/`, `app.py` | Chat interface, streaming, deployment |

## 🛠️ Tech Stack

- **LLM**: Groq (FREE - Llama 3.1)
- **Embeddings**: HuggingFace sentence-transformers (FREE - runs locally)
- **Vector Store**: FAISS (FREE - runs locally)
- **Web Search**: Tavily API
- **UI**: Streamlit
- **Framework**: LangChain

## 📁 Project Structure

```
rag-chatbot/
├── config/
│   ├── __init__.py
│   └── settings.py           # Configuration & API keys
├── core/
│   ├── __init__.py
│   ├── document_processor.py # Document loading & splitting
│   ├── embeddings.py         # HuggingFace embeddings
│   ├── vector_store.py       # FAISS operations
│   └── chain.py              # RAG chain orchestration
├── tools/
│   ├── __init__.py
│   └── tavily_search.py      # Web search integration
├── ui/
│   ├── __init__.py
│   ├── components.py         # Reusable UI components
│   └── chat_interface.py     # Chat logic
├── data/
│   ├── documents/            # Uploaded documents
│   └── faiss_index/          # Persisted vector index
├── app.py                    # Main Streamlit app
├── requirements.txt
└── README.md
```

## 🚀 Quick Start - Local Development

### Prerequisites

Install [uv](https://docs.astral.sh/uv/) - A fast Python package installer and resolver:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or use pip:
```bash
pip install uv
```

### 1. Clone and Setup Environment

**macOS/Linux:**
```bash
# Clone the repository
git clone <your-repo-url>
cd alma-GenAI-Project-AI-Advocate

# Create virtual environment with uv
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies with uv (much faster!)
uv pip install -r requirements.txt
```

**Windows (PowerShell):**
```powershell
# Clone the repository
git clone <your-repo-url>
cd alma-GenAI-Project-AI-Advocate

# Create virtual environment with uv
uv venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies with uv (much faster!)
uv pip install -r requirements.txt
```

**Windows (Command Prompt):**
```cmd
# Activate virtual environment
.venv\Scripts\activate.bat

# Install dependencies
uv pip install -r requirements.txt
```

### 2. Get API Keys (FREE!)

1. **Groq API Key** (FREE): https://console.groq.com/
   - Sign up and copy your API key
2. **Tavily API Key** (FREE tier): https://tavily.com/
   - Sign up and get your API key

### 3. Configure Environment Variables

**Option A: Using .env file (Recommended for local development)**

```bash
# Copy example file
cp .env.example .env

# Edit .env file with your actual keys (NO QUOTES!)
```

Your `.env` should look like this:
```bash
GROQ_API_KEY=gsk_your_actual_groq_key_here
TAVILY_API_KEY=tvly-your_actual_tavily_key_here
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.7
```

⚠️ **IMPORTANT**: 
- Do NOT use quotes around values
- Never commit `.env` to git (it's already in `.gitignore`)

**Option B: Using Streamlit Secrets (Also works locally)**

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_key_here"
TAVILY_API_KEY = "tvly-your_actual_tavily_key_here"
```

### 4. Run the Application

**All Platforms:**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 5. Using the Application

**Upload Documents:**
1. Click "Upload PDF Documents" in the sidebar
2. Upload your PDF files (e.g., legal documents, research papers, etc.)
3. Wait for processing to complete

**Ask Questions:**

Try these example queries:
- `"What is Personal Liberty: Procedure Established by Law?"`
- `"Summarize the main points about constitutional rights"`
- `"Explain the concept of due process"`
- `"What are the key differences between Article 21 and Article 22?"`

**Enable Web Search:**
- Toggle "Enable Web Search" to combine document knowledge with real-time web results
- Great for current events or topics not in your documents

## ☁️ Deployment to Streamlit Cloud

### Step 1: Prepare Repository

Make sure your code is in a GitHub repository:

```bash
# Initialize git (if not already done)
git init

# Add files (ensure .env is NOT committed!)
git add .
git commit -m "Initial commit"

# Push to GitHub
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click **"New app"**
3. Sign in with GitHub
4. Select your repository
5. Choose branch: `main`
6. Set main file path: `app.py`
7. Click **"Deploy"**

### Step 3: Add Secrets in Streamlit Cloud

After deployment:

1. Go to your app's dashboard
2. Click **"Settings"** → **"Secrets"**
3. Add your secrets in TOML format:

```toml
GROQ_API_KEY = "gsk_your_actual_groq_key_here"
TAVILY_API_KEY = "tvly-your_actual_tavily_key_here"
```

4. Click **"Save"**
5. Streamlit will automatically restart your app

### Important Security Notes 🔒

✅ **DO:**
- Use `.env` for local development
- Use Streamlit secrets for deployment
- Keep `.env` in `.gitignore`
- Rotate keys periodically

❌ **DON'T:**
- Never commit `.env` or `.streamlit/secrets.toml` to git
- Never share API keys in code or documentation
- Never use quotes in `.env` files

## 📖 SOLID Principles Applied

This project follows SOLID principles for maintainable code:

- **S**ingle Responsibility: Each module has one job
- **O**pen/Closed: Extensible without modifying existing code
- **L**iskov Substitution: Components can be swapped
- **I**nterface Segregation: Small, focused interfaces
- **D**ependency Inversion: Depend on abstractions

## 🎓 Teaching Notes

### Day 1: Foundations
- Explain RAG architecture (Retrieve → Augment → Generate)
- Walk through `config/settings.py` - environment variables
- Deep dive into `core/document_processor.py` - loaders & splitters
- **Hands-on**: Load and split a sample document

### Day 2: Vector Store
- Explain embeddings (text → vectors)
- Show `core/embeddings.py` - HuggingFace models
- Explain FAISS and similarity search
- Walk through `core/vector_store.py`
- **Hands-on**: Create embeddings and search

### Day 3: RAG Chain
- Explain LLM integration with Groq
- Walk through `core/chain.py` - prompt templates, chains
- Show `tools/tavily_search.py` - web search
- **Hands-on**: Build complete RAG pipeline

### Day 4: UI & Integration
- Explain Streamlit components
- Walk through `ui/components.py` and `ui/chat_interface.py`
- Show `app.py` - putting it all together
- **Hands-on**: Run the complete application

## � Troubleshooting

### API Key Issues

**Error: "Invalid API Key"**
- Verify your keys at [Groq Console](https://console.groq.com/) and [Tavily](https://tavily.com/)
- Make sure there are NO quotes in `.env` file
- Check if `.streamlit/secrets.toml` has placeholder values (should have real keys or not exist)
- Restart Streamlit after changing keys

**Error: "GROQ_API_KEY appears to be a placeholder"**
- Update `.streamlit/secrets.toml` with your actual keys
- OR delete `.streamlit/secrets.toml` to use `.env` instead

### Installation Issues

**Windows: "uv not found"**
- Make sure PowerShell execution policy allows scripts: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Try installing with pip: `pip install uv`

**macOS: Permission denied**
- Add execute permissions: `chmod +x ~/.cargo/bin/uv`

### Streamlit Issues

**App not loading**
- Check if port 8501 is already in use
- Try: `streamlit run app.py --server.port 8502`

**Secrets not loading**
- Ensure `.streamlit/secrets.toml` format is valid TOML
- Restart Streamlit completely (Ctrl+C and run again)

## 📝 License

MIT License - Feel free to use for teaching and learning!