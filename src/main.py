import json
import stt as stt_mod
from ai import LlamaCppClient

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

WAKE_WORD = config["wake_word"].lower()

print("Starting Wingman")

router = LlamaCppClient()

def handle_utterance(text: str):
    response = router.decipher_user_request(text)
    print(f"Model returned: {response!r}")

def main():
    listener = stt_mod.FasterWhisperVADListener()

    print(f"Listening for wake word: {WAKE_WORD!r}")
    for transcript in listener.listen_stream(yield_interim=False):
        if not transcript:
            continue

        print(f"TTS heard: {transcript!r}")

        text = transcript.lower()
        if WAKE_WORD not in text:
            print("Ignored, no wake word")
            continue

        command = text.split(WAKE_WORD, 1)[1].strip(" ,.!?")
        if not command:
            print("Wake word heard with no command")
            continue

        handle_utterance(command)

if __name__ == "__main__":
    main()
