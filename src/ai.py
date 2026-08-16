import json
import requests

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

class LlamaCppClient:
    endpoint = config["llama_cpp_endpoint"]

    def decipher_user_request(self, request):
        response = requests.post(f"{self.endpoint}/v1/chat/completions", json={
            'model': 'qwen-cmd',
            'messages': [
                {
                    'role': 'user',
                    'content': request,
                },
            ],
        })
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].lower().strip()
