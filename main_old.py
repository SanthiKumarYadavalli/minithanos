import os
from dotenv import load_dotenv
from RealtimeSTT import AudioToTextRecorder
import elevenlabs
import pyttsx3
from agents.god import do

load_dotenv()


def process_input(text):
    if "jarvis" in text.lower():
        print(text)
        response = do(text)
        print(response)
        speak_pyttsx3(response)


def speak_elevenlabs(text):
    audio = client.generate(
        voice="Nicole",
        voice_settings=elevenlabs.VoiceSettings(
            use_speaker_boost=True,
            speed=1,
            stability=0.5,
            similarity_boost=0.7,
            style=0.3,
        ),
        text=text,
        model="eleven_flash_v2_5"
    )
    elevenlabs.play(audio)
    

def speak_pyttsx3(text):
    pyttsx3.speak(text)


if __name__ == "__main__":
    client = elevenlabs.ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    recorder = AudioToTextRecorder(language="en", spinner=True)
    while True:
        text = recorder.text()
        process_input(text)
        recorder.stop()
