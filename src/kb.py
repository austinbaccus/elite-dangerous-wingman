import sys
import pydirectinput

def key_press(key):
    print(f"Pressing key: {key}", file=sys.stderr, flush=True)
    pydirectinput.press(key)
