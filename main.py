import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from google import genai

app = FastAPI()

# Setup templates directory
templates = Jinja2Templates(directory="app/templates")

# Initialize Gemini Client
# Assumes GEMINI_API_KEY is set in Render Environment Variables
client = genai.Client()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze_code(request: Request, code: str = Form(...)):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze this code and provide feedback/suggestions:\n\n{code}"
        )
        result = response.text
    except Exception as e:
        result = f"Error generating analysis: {str(e)}"
        
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "result": result, "code": code}
    )
