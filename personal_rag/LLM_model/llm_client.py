from openai import OpenAI


class LLMClient:
    def __init__(self):
        self.deepseek_client = OpenAI(api_key="xxx", base_url="https://api.deepseek.com")

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