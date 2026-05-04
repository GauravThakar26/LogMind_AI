# Task: Refactor Log Analyser for Cloud Deployment
**Agent Instructions — Execute tasks in order. Do not skip steps.**

---

## Context

This is a Python FastAPI web application for log file analysis.
Current setup uses a locally running Ollama model (gemma4:31b-cloud) which only works on the developer's machine.
Goal: Replace local Ollama inference with Google Gemini API and deploy the FastAPI app to Render.com so it works on any system worldwide.

---

## Step 1 — Audit the Project

- List all files in the project directory
- Read `main.py` (or equivalent FastAPI entry point)
- Identify every place where Ollama is called (look for `localhost:11434`, `ollama`, `requests.post` to local URLs)
- Read `requirements.txt`
- Note the current prompt structure being sent to Ollama — it must be preserved when switching to Gemini

---

## Step 2 — Create Environment File

- Check if `.env` file exists in project root; if not, create it
- Add the following line to `.env`:
  ```
  GEMINI_API_KEY=AIzaSyDpdpd7QXNnKwfEc_DOzUCEPQSM3KEqvms
  ```
- Check if `.gitignore` exists; if not, create it
- Ensure `.gitignore` contains `.env` — add it if missing
- **Never commit `.env` to git**

---

## Step 3 — Update Dependencies

In `requirements.txt`, add the following if not already present:
```
google-generativeai
python-dotenv
```

Run:
```bash
pip install google-generativeai python-dotenv
```

---

## Step 4 — Refactor Ollama Calls to Gemini

In `main.py` (or wherever Ollama is called):

**Remove or comment out** any code like:
```python
requests.post("http://localhost:11434/api/generate", ...)
```

**Add at the top of the file:**
```python
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel("gemini-2.5-flash")
```

**Replace the Ollama inference call with:**
```python
response = gemini_model.generate_content(prompt)
result_text = response.text
```

- Make sure the `prompt` variable being passed is exactly what was being sent to Ollama before
- If the original code parsed a JSON response from Ollama, parse `result_text` the same way using `json.loads(result_text)`
- If JSON parsing fails, wrap it in try/except and return a structured error response

---

## Step 5 — Add a Health Check Endpoint

In `main.py`, add this route if it does not already exist:
```python
@app.get("/health")
def health():
    return {"status": "ok"}
```
This is required for Render.com deployment to confirm the app is running.

---

## Step 6 — Create Render Deployment File

Create a file called `render.yaml` in the project root with this exact content:
```yaml
services:
  - type: web
    name: log-analyser
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        sync: false
```

> Note: `sync: false` means the API key must be manually entered on the Render dashboard — it will NOT be read from your local `.env` or committed to git. This is intentional and secure.

---

## Step 7 — Test Locally Before Pushing

Run the app locally:
```bash
uvicorn main:app --reload
```

- Open the browser at `http://localhost:8000`
- Upload a sample log file
- Verify that JSON output is returned correctly from Gemini
- If errors occur, read the terminal output and fix before proceeding

---

## Step 8 — Update README.md

Open or create `README.md` and ensure it contains the following sections:

```markdown
## Live Demo
[Add Render URL here after deployment]

## How It Works
1. Upload a log file via the browser
2. FastAPI backend sends the log content to Google Gemini API
3. Gemini returns structured JSON analysis
4. Results are rendered on the webpage

## Run Locally
1. Clone this repository
2. Get a free Gemini API key from https://aistudio.google.com
3. Create a `.env` file with: `GEMINI_API_KEY=your_key_here`
4. Run: `pip install -r requirements.txt`
5. Run: `uvicorn main:app --reload`
6. Open: http://localhost:8000
```

---

## Step 9 — Push to GitHub

```bash
git add .
git commit -m "refactor: replace Ollama with Gemini API, add Render deployment config"
git push origin main
```

Confirm the push succeeded and `.env` is NOT included in the committed files.

---

## Step 10 — Deploy on Render (Manual — Developer Action Required)

The following must be done by the developer manually in a browser:

1. Go to https://render.com and sign in (free account)
2. Click **New → Web Service**
3. Connect the GitHub repository for this project
4. Render will auto-detect `render.yaml`
5. Go to **Environment** settings and add:
   - Key: `GEMINI_API_KEY`
   - Value: (paste the actual key from aistudio.google.com)
6. Click **Deploy**
7. Wait for build to complete (~3–5 minutes)
8. Copy the live URL (format: `https://log-analyser.onrender.com`)
9. Update README.md with the live URL and push again

---

## Step 11 — Final Validation

- Open the live Render URL in a browser (not localhost)
- Upload a log file and confirm JSON output renders correctly
- Open the same URL on a mobile device or different machine to confirm it is globally accessible
- Record the demo screen using the live URL — not localhost

---

## Important Notes for the Agent

- Do NOT hardcode the API key anywhere in Python files
- Do NOT remove the file upload logic — only replace the inference backend
- If `main.py` is named differently (e.g., `app.py`), adjust all commands accordingly
- If the project uses a `Dockerfile` already, inform the developer before creating `render.yaml`
- Keep all existing routes, HTML templates, and frontend files intact
- If anything is ambiguous, read the relevant file first before making changes
