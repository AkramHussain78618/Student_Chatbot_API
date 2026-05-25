from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import google.generativeai as genai
import os

# ============================================================
# Configure Gemini API
# ============================================================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# ============================================================
# FastAPI setup
# ============================================================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ============================================================
# Home Route
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ============================================================
# Health Check Route
# ============================================================

@app.get("/health")
async def health():
    return {"message": "Server is working"}

# ============================================================
# Chat Route
# ============================================================

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
        print("ERROR:", str(e))

        return JSONResponse({
            "answer": f"Error: {str(e)}"
        })

# ============================================================
# Run Local Server
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )