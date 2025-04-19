from RealtimeSTT import AudioToTextRecorder
import asyncio
from agents.god import do
from live import audio_mode


def text_mode():
    while True:
        prompt = input(">>> ")
        if prompt == "exit":
            break
        if prompt:
            response = do(prompt)
            print("\n" + response + "\n")


if __name__ == "__main__":
    recorder = AudioToTextRecorder(language="en", spinner=True, ensure_sentence_ends_with_period=True)
    while True:
        try:
            # asyncio.run(audio_mode(recorder))
            text_mode()
        except Exception as e:
            print(type(e), e)