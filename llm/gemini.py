import google.generativeai as genai
from .base import LLMBase

class GeminiLLM(LLMBase):
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def chat(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"
