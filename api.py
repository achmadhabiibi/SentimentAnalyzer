"""
Sentiment Analyzer API
RESTful API built with FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
import os
import sys
import socket

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.sentiment_engine import SentimentAnalyzer

# ─── App Setup ──────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Sentiment Analyzer API",
    description="Indonesian & English Sentiment Analysis API",
    version="2.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentAnalyzer()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ─── Request Models ──────────────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"

class BulkAnalyzeRequest(BaseModel):
    texts: List[str]
    language: Optional[str] = "auto"


# ─── Pages ───────────────────────────────────────────────────────────────────

def read_template(name):
    path = os.path.join(BASE_DIR, "templates", name)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Template not found</h1>"

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(read_template("index.html"))

@app.get("/face", response_class=HTMLResponse)
async def face_page():
    return HTMLResponse(read_template("face.html"))


# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}

@app.post("/analyze")
async def analyze_single(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text tidak boleh kosong.")
    result = analyzer.analyze(request.text, request.language)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/analyze/bulk")
async def analyze_bulk(request: BulkAnalyzeRequest):
    if not request.texts:
        raise HTTPException(status_code=400, detail="List teks tidak boleh kosong.")
    if len(request.texts) > 50:
        raise HTTPException(status_code=400, detail="Maksimal 50 teks per request.")
    return analyzer.analyze_bulk(request.texts, request.language)

@app.get("/stats")
async def get_stats():
    return analyzer.get_stats()

@app.get("/history")
async def get_history(limit: int = 10):
    return {"history": analyzer.history[-min(limit,100):], "total": len(analyzer.history)}


# ─── Run ─────────────────────────────────────────────────────────────────────

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n" + "="*58)
    print("  🧠  SENTIMENT ANALYZER  v2.0 — WITH FACE DETECTION")
    print("="*58)
    print(f"  💻  Komputer ini  : http://localhost:8000")
    print(f"  📱  HP / Laptop lain (WiFi sama):")
    print(f"      http://{local_ip}:8000")
    print(f"  📷  Deteksi Wajah : http://localhost:8000/face")
    print(f"  📖  API Docs      : http://localhost:8000/docs")
    print("="*58)
    print("  ⚠️  Jangan tutup jendela ini selama dipakai!")
    print("  ⚠️  Tekan Ctrl+C untuk menghentikan server")
    print("="*58 + "\n")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
