import asyncio
import json
import time
import requests
from mcp.shared.memory import create_connected_server_and_client_session
import server as mcp_server

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

SYSTEM_PROMPT = """You are the flight computer of a spaceship in Elite Dangerous.
The pilot speaks a command. Call exactly one tool that carries it out.
Do not explain, do not ask questions, do not call more than one tool.
If no tool matches the command, reply with a single short sentence and call nothing."""

class LlamaCppClient:
    endpoint = config["llama_cpp_endpoint"]

    def __init__(self):
        self.tools = asyncio.run(self._load_tools())
        print(f"Loaded {len(self.tools)} ship commands from MCP server")

    async def _load_tools(self):
        async with create_connected_server_and_client_session(mcp_server.server) as session:
            result = await session.list_tools()
            return [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema,
                    },
                }
                for tool in result.tools
            ]

    async def _run_tool(self, name, arguments):
        async with create_connected_server_and_client_session(mcp_server.server) as session:
            result = await session.call_tool(name, arguments)
            return " ".join(block.text for block in result.content if getattr(block, "text", None)) # type: ignore

    def decipher_user_request(self, request):
        start = time.perf_counter()
        response = requests.post(f"{self.endpoint}/v1/chat/completions", json={
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": request,
                },
            ],
            "tools": self.tools,
            "tool_choice": "auto",
            "temperature": 0.0,
            "max_tokens": 900,
        })
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]

        calls = message.get("tool_calls")
        if not calls:
            return (message.get("content") or "").strip()

        results = []
        for call in calls:
            name = call["function"]["name"]
            arguments = json.loads(call["function"]["arguments"] or "{}")
            print(f"Calling MCP tool: {name} ({time.perf_counter() - start:.2f}s)")
            results.append(asyncio.run(self._run_tool(name, arguments)))
        return " ".join(r for r in results if r)
