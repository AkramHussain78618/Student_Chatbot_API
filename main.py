from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import google.generativeai as genai
import os

# ============================================================
# App setup
# ============================================================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ============================================================
# Gemini setup
# ============================================================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# ============================================================
# Home route
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ============================================================
# Chat route
# ============================================================

@app.post("/chat")
async def chat(request: Request):

    data = await request.json()
    question = data.get("question", "").strip()

    if not question:
        return JSONResponse({
            "answer": "Please ask something 🙂"
        })

    try:

        response = model.generate_content(question)

        return JSONResponse({
            "answer": response.text,
            "source": "Google Gemini AI"
        })

    except Exception as e:

        print("GEMINI ERROR:", str(e))

        return JSONResponse({
            "answer": f"Error: {str(e)}"
        })

# ============================================================
# Run locally
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )