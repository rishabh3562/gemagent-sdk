import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def configure(api_key=None):
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("Missing API key. Set `GOOGLE_API_KEY` or call `configure(api_key=...)`.")
    genai.configure(api_key=key)
