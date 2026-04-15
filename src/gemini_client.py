import os
from dotenv import load_dotenv
import google.generativeai as genai

from pathlib import Path

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")

print("Key loaded:", api_key is not None)
print("Key prefix:", api_key[:6] if api_key else None)

genai.configure(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash" 


def query_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(
        MODEL_NAME,
        generation_config={"temperature": 0.2}
    )

    response = model.generate_content(prompt)
    return response.text
