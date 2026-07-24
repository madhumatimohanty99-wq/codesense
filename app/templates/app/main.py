import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from google import genai

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=BASE_DIR)

# Render Environment Variable se key uthayega
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class CodeRequest(BaseModel):
    code: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_code(request: Request, code: str = Form(...)):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"You are a senior developer analyzing code. Point out bugs, improvements, and best practices:\n\n{code}"
        )
        feedback = response.text
    except Exception as e:
        feedback = f"Error: {str(e)}"
        
    return templates.TemplateResponse("index.html", {"request": request, "feedback": feedback, "code": code})