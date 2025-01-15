from openai import OpenAI
from personal_rag.config import get_api_key

class LLMClient:
    def __init__(self):
        api_key = get_api_key("deepseek")
        self.deepseek_client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    def ado_requests(self, prompt):
        response = self.deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content