import json
import os
import uvicorn
import kb
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.middleware.cors import CORSMiddleware

with open(os.path.join(os.path.dirname(__file__), "game_commands.json"), "r", encoding="utf-8") as f:
    COMMANDS = json.load(f)

server = FastMCP("wingman")

def press(name, times=1):
    for _ in range(times):
        kb.key_press(COMMANDS[name])
    return name

@server.tool(description="Send all power to shields. Use for max, full, or everything to shields or systems.")
def all_power_to_shields() -> str:
    return press("all power to shields", 4)

@server.tool(description="Send all power to engines. Use for max, full, or everything to engines.")
def all_power_to_engines() -> str:
    return press("all power to engines", 4)

@server.tool(description="Send all power to weapons. Use for max, full, or everything to weapons.")
def all_power_to_weapons() -> str:
    return press("all power to weapons", 4)

@server.tool(description="Reset power pips to a balanced distribution.")
def balance_power() -> str:
    return press("power re-distributed")

@server.tool(description="Cut power to shields, splitting it between engines and weapons.")
def cut_power_to_shields() -> str:
    press("power re-distributed")
    press("all power to engines", 2)
    press("all power to weapons", 2)
    return "cutting power to shields"

@server.tool(description="Cut power to engines, splitting it between shields and weapons.")
def cut_power_to_engines() -> str:
    press("power re-distributed")
    press("all power to shields", 2)
    press("all power to weapons", 2)
    return "cutting power to engines"

@server.tool(description="Cut power to weapons, splitting it between shields and engines.")
def cut_power_to_weapons() -> str:
    press("power re-distributed")
    press("all power to shields", 2)
    press("all power to engines", 2)
    return "cutting power to weapons"

@server.tool(description="Target a sub-system on the currently selected ship.")
def target_subsystem() -> str:
    return press("targeting sub-system")

@server.tool(description="Launch chaff to break missile and gimballed weapon locks.")
def deploy_chaff() -> str:
    return press("deploying chaff")

@server.tool(description="Launch a heat sink to dump heat.")
def deploy_heat_sink() -> str:
    return press("deploying heat sink")

@server.tool(description="Fire a shield cell bank to restore shields.")
def activate_shield_cell() -> str:
    return press("activating shield cell")

@server.tool(description="Toggle silent running on or off.")
def toggle_silent_running() -> str:
    return press("engaging silent running")

@server.tool(description="Jettison all cargo.")
def jettison_cargo() -> str:
    return press("jettisoning cargo")

@server.tool(description="Toggle the cargo scoop open or closed. The game toggles, so this both deploys and retracts it.")
def toggle_cargo_scoop() -> str:
    return press("deploying cargo scoop")

@server.tool(description="Toggle the landing gear up or down. The game toggles, so this both deploys and retracts it.")
def toggle_landing_gear() -> str:
    return press("deploying landing gear")

@server.tool(description="Toggle the ship lights on or off. The game toggles, so this both activates and deactivates them.")
def toggle_lights() -> str:
    return press("activating lights")

@server.tool(description="Toggle night vision on or off. The game toggles, so this both activates and deactivates it.")
def toggle_night_vision() -> str:
    return press("activating night vision")

@server.tool(description="Charge the frame shift drive to jump or supercruise. Use for engage, jump, or FSD.")
def charge_frame_shift_drive() -> str:
    return press("frame shift drive charging")

@server.tool(description="Launch the ship-launched fighter.")
def deploy_fighter() -> str:
    return press("deploying fighters")

@server.tool(description="Recall the ship-launched fighter back to the hangar.")
def recall_fighter() -> str:
    return press("recalling fighters")

@server.tool(description="Order the fighter to defend.")
def order_fighters_to_defend() -> str:
    return press("ordering fighters to defend")

@server.tool(description="Order the fighter to follow.")
def order_fighters_to_follow() -> str:
    return press("ordering fighters to follow")

if __name__ == "__main__":
    app = server.streamable_http_app(
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id", "Mcp-Protocol-Version"],
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)
