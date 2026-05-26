from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os

app = FastAPI()

# Static + Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

# Chat route
@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, question: str = Form(...)):

    answer = ""

    try:
        response = model.generate_content(question)
        answer = response.text

    except Exception as e:
        answer = f"Error: {str(e)}"

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "question": question,
            "answer": answer
        }
   