from fastapi import FastAPI
from fastapi.responses import JSONResponse
import google.generativeai as genai
import os

app = FastAPI()

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

@app.get("/")
async def home():
    return {"message": "Server is working"}

@app.post("/chat")
async def chat():

    try:

        response = model.generate_content("What is AI?")

        return JSONResponse({
            "answer": response.text
        })

    except Exception as e:

        return JSONResponse({
            "error": str(e)
        })