from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import google.generativeai as genai
import os

app = FastAPI()

# Static + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# Chat API
@app.post("/chat")
async def chat(request: Request):

    try:

        data = await request.json()

        question = data.get("question", "").strip()

        if not question:
            return JSONResponse({
                "answer": "Please ask something."
            })

        response = model.generate_content(question)

        return JSONResponse({
            "answer": response.text
        })

    except Exception as e:

        return JSONResponse({
            "answer": f"Error: {str(e)}"
        })

# Local run
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000
    )