# Deployment Guide - Streamlit Cloud

## Secure Deployment Without Committing Passwords

### Option 1: Streamlit Cloud (Recommended) ⭐

**Step 1: Prepare Your Repository**
```bash
# Make sure .env and secrets.toml are in .gitignore
git add .gitignore
git commit -m "Add .env and secrets to gitignore"
git push
```

**Step 2: Deploy to Streamlit Cloud**
1. Go to [streamlit.io](https://streamlit.io)
2. Click "Deploy an app" → Sign in with GitHub
3. Select your repository
4. Choose branch: `main`
5. Set Main file path: `app.py`
6. Click "Deploy"

**Step 3: Add Secrets in Dashboard**
1. After deployment, go to your app's settings
2. Click "Settings" → "Secrets"
3. Add your secrets in TOML format:
```toml
GROQ_API_KEY = "your_actual_groq_key"
TAVILY_API_KEY = "your_actual_tavily_key"
HUGGINGFACE_API_KEY = "your_actual_huggingface_key"
```
4. Click "Save" → Streamlit will restart your app

### Option 2: Docker + Environment Variables

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Run locally:**
```bash
docker build -t my-rag-app .
docker run -e GROQ_API_KEY="your_key" -e TAVILY_API_KEY="your_key" -p 8501:8501 my-rag-app
```

### Option 3: Environment Variables (Any Cloud Platform)

**Use these environment variables:**
- `GROQ_API_KEY` - Your Groq API key
- `TAVILY_API_KEY` - Your Tavily API key
- `HUGGINGFACE_API_KEY` - Your HuggingFace token (if needed)

Each cloud platform has different ways to set secrets:

**Heroku:**
```bash
heroku config:set GROQ_API_KEY="your_key"
heroku config:set TAVILY_API_KEY="your_key"
```

**AWS:**
- Use AWS Secrets Manager
- Reference in environment variables

**Google Cloud:**
- Use Google Cloud Secret Manager
- Reference in Cloud Run environment

## Local Development

1. Create `.streamlit/secrets.toml` with your keys:
```toml
GROQ_API_KEY = "sk-..."
TAVILY_API_KEY = "tvly-..."
```

2. Run locally:
```bash
streamlit run app.py
```

## Security Best Practices ✅

1. ✅ Never commit `.env` or `.streamlit/secrets.toml`
2. ✅ Always use environment variables or secrets managers
3. ✅ Rotate keys periodically
4. ✅ Use different keys for dev/prod
5. ✅ Never share API keys in code or documentation

## Troubleshooting

**"API Key not found"**
- Check that secrets are added to Streamlit dashboard
- Restart your app after adding secrets
- Verify the exact key names match

**"ModuleNotFoundError: streamlit"**
- Make sure `requirements.txt` includes `streamlit>=1.38.0`
- Run `pip install -r requirements.txt`

**Secrets not loading in local development**
- Ensure `.streamlit/secrets.toml` exists
- Check file format is valid TOML
- Restart Streamlit: `streamlit run app.py`
