import json
import time
import stt as stt_mod
from ai import LlamaCppClient
from game import is_elite_dangerous_running

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

WAKE_WORD = config["wake_word"].lower()
POLL_SECONDS = 5

print("Starting Wingman")

router = LlamaCppClient()

def handle_utterance(text: str):
    print(f"STT heard: {text!r}")
    response = router.decipher_user_request(text)
    print(f"Model returned: {response!r}")

def main():
    listener = stt_mod.FasterWhisperVADListener()

    while True:
        if not is_elite_dangerous_running():
            print("Elite Dangerous is not running, waiting")
            while not is_elite_dangerous_running():
                time.sleep(POLL_SECONDS)
            print("Elite Dangerous detected")

        stream = listener.listen_stream(yield_interim=False)
        print(f"Listening for wake word: {WAKE_WORD!r}")
        try:
            for transcript in stream:
                if not is_elite_dangerous_running():
                    break

                if not transcript:
                    continue

                # print(f"STT heard: {transcript!r}")

                text = transcript.lower()
                if WAKE_WORD not in text:
                    # print("Ignored, no wake word")
                    continue

                command = text.split(WAKE_WORD, 1)[1].strip(" ,.!?")
                if not command:
                    # print("Wake word heard with no command")
                    continue

                handle_utterance(command)
        finally:
            stream.close()

if __name__ == "__main__":
    main()
