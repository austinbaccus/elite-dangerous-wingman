# Wingman MCP Server

MCP server exposing Elite Dangerous ship commands as tools. Each tool presses the real key via `kb.py`, so **the game receives actual input** when a tool is called.

Runs over **streamable HTTP** on port `8000` at path `/mcp`, bound to `0.0.0.0` so it is reachable from other machines on the LAN.

## Tools

| Group | Tools |
| --- | --- |
| Power | `all_power_to_shields`, `all_power_to_engines`, `all_power_to_weapons`, `balance_power`, `cut_power_to_shields`, `cut_power_to_engines`, `cut_power_to_weapons` |
| Combat | `target_subsystem`, `deploy_chaff`, `deploy_heat_sink`, `activate_shield_cell`, `toggle_silent_running`, `jettison_cargo` |
| Ship | `toggle_cargo_scoop`, `toggle_landing_gear`, `toggle_lights`, `toggle_night_vision`, `charge_frame_shift_drive` |
| Fighters | `deploy_fighter`, `recall_fighter`, `order_fighters_to_defend`, `order_fighters_to_follow` |

Key bindings come from `game_commands.json` — the single source of truth. Rebind in-game, edit it here, and every tool follows.

Several commands are **toggles in Elite**: gear, lights, night vision, and cargo scoop each use one key for both directions. There is no `turn_on_lights` / `turn_off_lights` pair because both would press the same key and the game would just toggle. The tools are named `toggle_*` to be honest about that.

The power tools send multi-press sequences: `all_power_to_*` presses its direction four times, and `cut_power_to_*` balances first, then moves two pips to each of the other two systems.

`noop` exists in `game_commands.json` with an empty key and is deliberately not exposed — with tool calling, the model simply calls nothing when no command matches.

## Sending real keystrokes

`SendInput` delivers to the **foreground window**. Trigger a tool from a browser and the keystroke goes to the browser, not to Elite. To test for real, Elite must be focused when the call fires.

Two more constraints:

- If Elite runs elevated, this server must run elevated too. Windows silently drops input from a lower-integrity process — no error, no keypress.
- Borderless windowed accepts synthetic input far more reliably than exclusive fullscreen.

## Install

Requires the **2.x** SDK, which exports `MCPServer` from `mcp.server`. On 1.x this server will not import, since 1.x uses the older `mcp.server.fastmcp.FastMCP` path.

```bash
pip install "mcp>=2.0" uvicorn pydirectinput
```

Check what you have with `pip show mcp`. Note the repo has a venv at `src\.venv` — activate it before installing, or you will install into a different interpreter than the one you run.

## Run it

```bash
python X:\source\repos\elite-dangerous-wingman\mcp\server.py
```

Endpoint: `http://<this-machine-ip>:8000/mcp` — the `/mcp` path is required.

If you get `WinError 10048`, port 8000 is already held by a previous instance. Find and stop it:

```bash
netstat -ano | findstr :8000
```

## Connect from the llama.cpp WebUI

Paste the endpoint into the WebUI's MCP server field. Two settings in `server.py` exist specifically to make this work, and removing either breaks the browser connection:

- **CORS middleware.** The WebUI is served from a different port, so the browser treats the MCP server as cross-origin. Without `Access-Control-Allow-Origin` the browser aborts the request before it reaches the server, and the UI reports `NetworkError when attempting to fetch resource` while the server logs nothing at all.
- **`enable_dns_rebinding_protection=False`.** The SDK validates the `Origin` header by default and answers a browser request with `403 Invalid Origin header`. Unlike the CORS failure, this one *does* appear in the server log.

`Mcp-Session-Id` is in `expose_headers` because the streamable HTTP transport returns the session id as a response header; if the browser cannot read it, the session breaks immediately after `initialize`.

`allow_origins=["*"]` and disabled rebinding protection are fine for a LAN test server that only prints messages. Tighten both to the WebUI's actual origin if this ever does something real.

## Verify without a browser

```bash
curl -i -X POST http://127.0.0.1:8000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2025-06-18\",\"capabilities\":{},\"clientInfo\":{\"name\":\"curl\",\"version\":\"1.0\"}}}"
```

A healthy response is `200`, a `mcp-session-id` header, and an SSE `event: message` frame naming `"serverInfo":{"name":"wingman"}`.

## Inspect it in a UI

The MCP Inspector gives you a browser UI to list and invoke the tools. Requires Node.

```bash
npx @modelcontextprotocol/inspector
```

Choose transport **Streamable HTTP**, enter the endpoint, then **Connect** → **List Tools**. Tool output appears in the response pane; the stderr messages appear in the terminal running `server.py`.

## Register it with Claude Code

```bash
claude mcp add --transport http wingman http://127.0.0.1:8000/mcp
```

Then `claude mcp list` to verify. Inside a session the tools are exposed as `mcp__wingman__deploy_landing_gear` and `mcp__wingman__turn_on_lights`. Remove it with `claude mcp remove wingman`.

## Note on llama.cpp itself

The llama.cpp **WebUI** is an MCP client and can call this server, as above. The llama.cpp **server API** is not — `/v1/chat/completions` only accepts a `tools` array and returns `tool_calls`. Wiring this server into `src/main.py` means the Python app acts as the MCP client: read the tool schemas from here, pass them as `tools`, then dispatch any returned `tool_calls` back to this server.
