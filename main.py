# ============================================================
# main.py - ChatGPT-like AI Chatbot (Render Ready)
# ============================================================

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
from openai import OpenAI

# ============================================================
# App setup
# ============================================================

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ============================================================
# OpenAI Client (API KEY from Render ENV)
# ============================================================

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================================================
# Home route
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ============================================================
# Chat route (ChatGPT-like AI)
# ============================================================

@app.post("/chat")
async def chat(request: Request):

    data = await request.json()
    question = data.get("question", "").strip()

    if not question:
        return JSONResponse({
            "answer": "Please ask something 🙂",
            "source": "system"
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, friendly AI study assistant chatbot. "
                        "Explain answers in simple language for students."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7
        )

        answer = response.choices[0].message.content

        return JSONResponse({
            "answer": answer,
            "source": "OpenAI GPT"
        })

    except Exception as e:
    print("OPENAI ERROR:", str(e))

    return JSONResponse({
        "answer": f"Error: {str(e)}",
        "source": "system"
    })

# ============================================================
# Run locally
# ============================================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Server running at http://127.0.0.1:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)