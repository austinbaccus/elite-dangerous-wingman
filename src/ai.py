from ollama import Client

class OllamaClient:
    client = Client(host='http://localhost:11434', headers={'x-some-header': 'some-value'})

    def decipher_user_request(self, request):
        response = self.client.chat(model='qwen-cmd', messages=[
            {
                'role': 'user',
                'content': request,
            },
        ])
        return response.message.content.lower().strip()