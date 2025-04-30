from ollama import chat, ChatResponse
from all_tools import FUNCTIONS
from utils import get_files_list

base_prompt = """
Don't call tools if you don't need to.
"""
model = "llama3.1:8b"
files_list = get_files_list()
messages = [
    {"role": "user", "content": base_prompt + "\nHere's my files list:\n" + str(files_list)}
]
chat(model=model, messages=messages)


def get_chat(prompt):
    global files_list, messages
    new_files_list = get_files_list()
    if new_files_list != files_list:
        files_list = new_files_list
        prompt += "\nHere's my files list:\n" + str(files_list)
    messages += [{"role": "user", "content": prompt}]
    return chat(
        model=model,
        messages= messages,
        tools=list(FUNCTIONS.values()),
    )


def do_thing(prompt):
  response: ChatResponse = get_chat(prompt)

  if response.message.tool_calls:
    # There may be multiple tool calls in the response
    for tool in response.message.tool_calls:
      # Ensure the function is available, and then call it
      if function_to_call := FUNCTIONS.get(tool.function.name):
        print('Calling function:', tool.function.name)
        print('Arguments:', tool.function.arguments)
        output = function_to_call(**tool.function.arguments)
        print('Function output:', output)
      else:
        print('Function', tool.function.name, 'not found')

  # Only needed to chat with the model using the tool call results
  if response.message.tool_calls:
    # Add the function response to messages for the model to use
    messages.append(response.message)
    messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

    # Get final response from model with function outputs
    final_response = chat(model, messages=messages)
    print('Final response:', final_response.message.content)

  else:
    print('No tool calls returned from model')


def main():
    prompt = "Hello, how are you?"
    do_thing(prompt)
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
        do_thing(user_input)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
