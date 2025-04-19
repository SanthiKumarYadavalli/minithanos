from .client import client
from google.genai import types
from tools import FUNCTIONS

base_prompt = """
You are an all-powerful assistant with access to a wide range of tools. Use them skillfully.

Please:
- Respond to me in a friendly, conversational tone.
- Clearly understand and utilize the tools at your disposal.
- When I ask you to perform a task, use the most appropriate tool with the correct arguments.
- If you're unsure how to complete a task directly, attempt to run a command that could solve it.
- Remember that I'm using a Windows operating system — consider that when giving instructions or running commands.

Act confidently and helpfully. Let’s get things done.
"""

model = "gemini-2.0-flash-lite"
generate_content_config = types.GenerateContentConfig(
    temperature=2,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
    system_instruction=[
        types.Part.from_text(text="""give short responses like in a chat"""),
    ],
    tools=list(FUNCTIONS.values()),
)

chat = client.chats.create(model=model, config=generate_content_config)
chat.send_message(message=base_prompt)


def generate(prompt):
    return chat.send_message(prompt)

