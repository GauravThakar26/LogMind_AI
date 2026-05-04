from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routes.analyze import router as analyze_router

app = FastAPI()

# Correct the path to the frontend public directory
# Render runs 'cd backend && uvicorn...', so we need to go up one level to find frontend
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(base_dir, "frontend", "public")

# Fallback if the above fails (for local development)
if not os.path.exists(frontend_path):
    frontend_path = os.path.join(os.getcwd(), "..", "frontend", "public")
    frontend_path = os.path.abspath(frontend_path)

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router, prefix="/api")

@app.get("/")
def root():
    # Serve the index.html file as the home page
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"status": "AI Log Reviewer running", "message": "Frontend not found at " + index_file}

@app.get("/health")
def health():
    return {"status": "ok"}
