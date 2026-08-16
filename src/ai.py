import json
import requests

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open("m", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().split("<|im_start|>system")[1].split("<|im_end|>")[0].strip()

class LlamaCppClient:
    endpoint = config["llama_cpp_endpoint"]

    def decipher_user_request(self, request):
        response = requests.post(f"{self.endpoint}/v1/chat/completions", json={
            'messages': [
                {
                    'role': 'system',
                    'content': SYSTEM_PROMPT,
                },
                {
                    'role': 'user',
                    'content': request,
                },
            ],
            'temperature': 0.0,
            'top_p': 1,
            'repeat_penalty': 1.2,
            'repeat_last_n': 128,
            #'max_tokens': 3,
            'stop': ["\n", "\r"],
        })
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].lower().strip()
