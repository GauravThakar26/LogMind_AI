import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
gemini_model = genai.GenerativeModel(os.environ.get("GEMINI_MODEL_NAME", "gemini-3.1-flash-lite"))
