from google import genai
import pyaudio
from google.genai import types
from tools import FUNCTIONS
from dotenv import load_dotenv
import os
import asyncio
from RealtimeSTT import AudioToTextRecorder

load_dotenv()

name = "Charlie"
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),
                      http_options={'api_version': 'v1alpha'})
model = "gemini-2.0-flash-exp"
config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    tools=list(FUNCTIONS.values()) + [{"google_search": {}}],
    system_instruction=types.Content(
        parts=[
            types.Part(
                text=f"You are a Jarvis-like assistant '{name}'. You can do anything the user asks you to do with the tools you have. answer in a friendly tone. Don't give long responses. Give only SHORT responses.",
            )
        ]
    ),
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Aoede")
        )
    ),
)


async def async_enumerate(it):
    n = 0
    async for item in it:
        yield n, item
        n += 1

p = pyaudio.PyAudio()


async def handle_tool_call(session, tool_call):
    for fc in tool_call.function_calls:
        f = FUNCTIONS[fc.name]
        tool_response = types.LiveClientToolResponse(
            function_responses=[
                types.FunctionResponse(
                    name=fc.name,
                    id=fc.id,
                    response=f(**fc.args),
                )
            ]
        )
    await session.send(input=tool_response)
    

prev_prompt = ""
awake = False


async def audio_mode(recorder):
    global prev_prompt, awake
    while True:
        print("SESSION STARTED!")
        async with client.aio.live.connect(model=model, config=config) as session:
            while True:
                if prev_prompt:
                    message = prev_prompt
                    prev_prompt = ""
                else:
                    message = recorder.text()
                try:
                    stream = p.open(format=p.get_format_from_width(2),
                                    channels=1,
                                    rate=24000,
                                    output=True)
                    # print(message)
                    recorder.stop()
                    if name.lower() in message.lower() or awake:
                        awake = True
                        await session.send(input=message, end_of_turn=True)
                        async for idx, response in async_enumerate(session.receive()):
                            if response.text is not None:
                                print(response.text, end="")
                            if response.tool_call is not None:
                                await handle_tool_call(session, response.tool_call)
                            if response.data is not None: 
                                stream.write(response.data)
                        if 'bye' in message.lower():
                            awake = False
                    stream.close()
                except Exception as e:
                    prev_prompt = message
                    print(e)
                    break


if __name__ == "__main__":
    recorder = AudioToTextRecorder(language="en", spinner=True, ensure_sentence_ends_with_period=True)
    while True:
        try:
            asyncio.run(audio_mode(recorder))
            # text_mode()
        except Exception as e:
            print(type(e), e)
