import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.dirname(BASE_DIR))

client = OpenAI(api_key="sk-proj-abc123yourrealactualkeyhere...")

class CodeRequest(BaseModel):
    code: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
   return templates.TemplateResponse(request, "index.html")

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior developer analyzing code. Point out bugs, security risks, and optimization suggestions clearly."},
                {"role": "user", "content": f"Analyze this code:\n\n{request.code}"}
            ]
        )
        return {"analysis": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}