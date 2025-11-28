import requests
from .base import LLMBase

class BananaLLM(LLMBase):
    def __init__(self, api_key: str, model_key: str, url: str):
        self.api_key = api_key
        self.model_key = model_key
        self.url = url

    def chat(self, prompt: str) -> str:
        # This is a generic implementation for a REST API
        # Adjust the payload structure according to the specific API documentation for Nano Banana Pro
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_key,
            "messages": [{"role": "user", "content": prompt}],
            # Add other parameters like temperature, max_tokens if needed
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Assuming standard OpenAI-like response or similar. Adjust parsing logic as needed.
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            elif 'output' in data:
                return data['output']
            else:
                return str(data)
        except Exception as e:
            return f"Banana Error: {str(e)}"
