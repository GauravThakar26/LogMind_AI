from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.routes.analyze import router as analyze_router

app = FastAPI()

# Mount the frontend directory to serve static assets (CSS, JS, Images)
# This allows the browser to find files like /static/css/style.css
frontend_path = os.path.join(os.getcwd(), "frontend", "public")
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
