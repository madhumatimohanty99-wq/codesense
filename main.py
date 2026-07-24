import os
from pathlib import Path
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai

app = FastAPI()

# Setup templates directory using path resolution
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

# Initialize Gemini Client (Capital C)
client = genai.Client()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html"
    )

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_code(request: Request, code: str = Form(...)):
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Analyze this code and provide feedback/suggestions:\n\n{code}"
        )
        result = response.text
    except Exception as e:
        result = f"Error generating analysis: {str(e)}"

    return result
