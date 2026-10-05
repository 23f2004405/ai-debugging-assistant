from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.graph import agent
from app.schemas import SupportRequest

app = FastAPI(title="AI Support Engineer", version="1.0.0")

INDEX = Path("app/static/index.html")

@app.get("/", response_class=HTMLResponse)
def home():
    return INDEX.read_text(encoding="utf-8")

@app.post("/support")
def support(request: SupportRequest):
    result = agent.invoke({"issue": request.issue})
    return result["answer"]
