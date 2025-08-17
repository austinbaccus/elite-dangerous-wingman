# pip install faster-whisper webrtcvad sounddevice numpy
import collections, queue, time
import numpy as np
import sounddevice as sd
import webrtcvad
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
FRAME_MS = 30            # WebRTC VAD needs 10/20/30ms frames
SILENCE_TAIL_MS = 500    # how much trailing silence ends an utterance
DEVICE = "cpu"           # "cuda" or "cpu"
DEVICE_INDEX = 1         # which gpu you want to use (idk what happens for cpu)
MODEL_NAME = "base.en"
COMPUTE_TYPE = "int8"    # "int8" (smallest), or "int8_float16" (faster on GPU)

def _frame_bytes(int16_pcm):
    return (int16_pcm.tobytes(), len(int16_pcm))

class FasterWhisperVADListener:
    def __init__(self, input_device=None):
        self.model = WhisperModel(MODEL_NAME, device=DEVICE, compute_type=COMPUTE_TYPE) #device_index=DEVICE_INDEX, 
        self.vad = webrtcvad.Vad(2)  # 0=aggresive->3=most aggressive; 2 is a good middle
        self.blocksize = int(SAMPLE_RATE * FRAME_MS / 1000)  # samples per 30ms frame
        self.q = queue.Queue()
        self.input_device = input_device

    def _audio_cb(self, indata, frames, time_info, status):
        if status:
            print("Audio status:", status)
        # indata is float32 in [-1,1]; convert to int16 for VAD
        int16_pcm = np.clip(indata[:, 0], -1, 1)
        int16_pcm = (int16_pcm * 32767).astype(np.int16)
        self.q.put(int16_pcm)

    def listen_stream(self, yield_interim=False):
        ring = collections.deque()
        speech_active = False
        last_speech_time = 0.0
        utterance = []

        with sd.InputStream(samplerate=SAMPLE_RATE, blocksize=self.blocksize,
                            channels=1, dtype='float32', callback=self._audio_cb,
                            device=self.input_device):
            while True:
                block = self.q.get()  # int16, length = blocksize
                now = time.time()
                is_speech = self.vad.is_speech(_frame_bytes(block)[0], SAMPLE_RATE)

                if is_speech:
                    speech_active = True
                    last_speech_time = now
                    utterance.append(block)
                else:
                    # keep a little context in case VAD trims too tight
                    ring.append(block)
                    if len(ring) > int((SILENCE_TAIL_MS / FRAME_MS)):
                        ring.popleft()

                # if we had speech and now enough silence -> finalize
                if speech_active and (now - last_speech_time) * 1000 >= SILENCE_TAIL_MS:
                    # finalize segment = utterance + small trailing context
                    segment = np.concatenate(utterance + list(ring)) if utterance else None
                    ring.clear()
                    speech_active = False
                    utterance = []
                    if segment is None:
                        continue

                    # Convert int16 -> float32 [-1,1] for faster-whisper
                    audio_f32 = (segment.astype(np.float32) / 32768.0)

                    # Run ASR (no VAD here; we already segmented)
                    segments, _ = self.model.transcribe(audio_f32,
                                                        vad_filter=True,
                                                        no_speech_threshold=0.7,
                                                        condition_on_previous_text=False)
                    text = " ".join(s.text for s in segments).strip()
                    if text:
                        yield text

if __name__ == "__main__":
    listener = FasterWhisperVADListener()
    print("Listening for voice commands (faster-whisper + VAD)")
    for transcript in listener.listen_stream(yield_interim=False):
        print(f"Whisper heard: {transcript!r}")