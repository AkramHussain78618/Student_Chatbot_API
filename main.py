from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os

# ============================================================
# Gemini API Setup
# ============================================================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

# ============================================================
# FastAPI App
# ============================================================

app = FastAPI()

# ============================================================
# Home Route
# ============================================================

@app.get("/")
async def home():
    return {"message": "AI Chatbot Running Successfully"}

# ============================================================
# Chat Route
# ============================================================

@app.post("/chat")
async def chat(request: Request):

    try:
        data = await request.json()

        question = data.get("question")

        if not question:
            return JSONResponse({
                "answer": "Please ask something"
            })

        response = model.generate_content(question)

        return JSONResponse({
            "answer": response.text
        })

    except Exception as e:

        print("ERROR:", str(e))

        return JSONResponse({
            "answer": str(e)
        })