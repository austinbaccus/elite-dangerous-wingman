import stt as stt_mod
from ai import LlamaCppClient

print("Starting Wingman")

router = LlamaCppClient()

def handle_utterance(text: str):
    response = router.decipher_user_request(text)
    print(f"Model returned: {response!r}")

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
