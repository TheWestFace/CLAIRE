import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash-lite"


def query_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME, generation_config={"temperature": 0.2})

    response = model.generate_content(prompt)
    return response.text
