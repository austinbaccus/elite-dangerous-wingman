import json
import stt as stt_mod
import kb as kb_mod
from ai import OllamaClient

print("Starting Wingman")

idx_commands = {
    "1":  "all power to shields",
    "2":  "all power to engines",
    "3":  "all power to weapons",
    "4":  "cutting power to shields",
    "5":  "cutting power to engines",
    "6":  "cutting power to weapons",
    "7":  "power re-distributed",
    "8":  "targeting sub-system",
    "9":  "deploying chaff",
    "10": "engaging silent running",
    "11": "jettisoning cargo",
    "12": "deploying cargo scoop",
    "13": "retracting cargo scoop",
    "14": "deploying landing gear",
    "15": "retracting landing gear",
    "16": "deploying fighters",
    "17": "recalling fighters",
    "18": "ordering fighters to defend",
    "19": "ordering fighters to follow",
    "20": "activating lights",
    "21": "deactivating lights",
    "22": "activating night vision",
    "23": "deactivating night vision",
    "24": "frame shift drive charging",
    "25": "activating shield cell",
    "26": "deploying heat sink",
    "27": "noop",
}

with open("game_commands.json", "r", encoding="utf-8") as f:
    commands = json.load(f)

router = OllamaClient()

def repeat_key_n_times(key, n):
    for i in n:
        kb_mod.key_press(key)

def pip_no_shields():
    kb_mod.key_press(idx_commands["7"])
    kb_mod.key_press(idx_commands["2"])
    kb_mod.key_press(idx_commands["2"])
    kb_mod.key_press(idx_commands["3"])
    kb_mod.key_press(idx_commands["3"])

def pip_no_engines():
    kb_mod.key_press(idx_commands["7"])
    kb_mod.key_press(idx_commands["1"])
    kb_mod.key_press(idx_commands["1"])
    kb_mod.key_press(idx_commands["3"])
    kb_mod.key_press(idx_commands["3"])

def pip_no_weapons():
    kb_mod.key_press(idx_commands["7"])
    kb_mod.key_press(idx_commands["1"])
    kb_mod.key_press(idx_commands["1"])
    kb_mod.key_press(idx_commands["2"])
    kb_mod.key_press(idx_commands["2"])

def handle_utterance(text: str):
    cmd = router.decipher_user_request(text)
    print(f"Qwen interpreted this as: {idx_commands[cmd]!r}")

    # PIP management requires multiple button presses
    if int(cmd) <= 3:   # all power to shields/engines/weapons
        action = lambda: repeat_key_n_times(commands[idx_commands[cmd]], 4)
    elif int(cmd) is 4: # no shields
        action = lambda: pip_no_shields()
    elif int(cmd) is 5: # no engines
        action = lambda: pip_no_engines()
    elif int(cmd) is 6: # no weapons
        action = lambda: pip_no_weapons()
    else:               # normal command
        action = lambda: kb_mod.key_press(commands[idx_commands[cmd]])
    action()

def main():
    listener = stt_mod.FasterWhisperVADListener()

    print("Listening for voice commands")
    for transcript in listener.listen_stream(yield_interim=False):
        if not transcript:
            continue

        print(f"TTS heard: {transcript!r}")

        handle_utterance(transcript)

if __name__ == "__main__":
    main()
