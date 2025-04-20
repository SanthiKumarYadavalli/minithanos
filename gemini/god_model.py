from .client import client
from google.genai import types
from all_tools import FUNCTIONS
from utils import get_files_list

base_prompt = """
You are an all-powerful assistant with access to a wide range of tools. Use them skillfully.

Please:
- Respond to me in a friendly, conversational tone.
- Clearly understand and utilize the tools at your disposal.
- When I ask you to perform a task, use the most appropriate tool with the correct arguments.
- If you're unsure how to complete a task directly, attempt to run a command that could solve it.

Act confidently and helpfully. Let’s get things done.
Don't ask me if you can do something, just do it.
"""

model = "gemini-2.0-flash"
generate_content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
    system_instruction=[
        types.Part.from_text(text="""give very short responses like in a chat"""),
    ],
    tools=list(FUNCTIONS.values()),
)

chat = client.chats.create(model=model, config=generate_content_config)
files_list = get_files_list()
chat.send_message(message=base_prompt + "\n\n Here's my filesystem:\n" + get_files_list())


def generate(prompt):
    global files_list
    if files_list != get_files_list():
        files_list = get_files_list()
        chat.send_message(message="\n\n Here's my filesystem:\n" + get_files_list())
    return chat.send_message(prompt)
