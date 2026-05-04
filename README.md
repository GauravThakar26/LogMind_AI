# AI Log Reviewer

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
