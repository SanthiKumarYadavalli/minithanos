from gemini import shortcutter_model
from utils import press_shortcut

def perform_shortcut(task: str) -> dict:
    """
    Generate a shortcut for a given task and press it.
    Args:
        task (str): The task to generate a shortcut from.
    Returns:
        dict: The result of the operation
    """
    print("Shortcutter called!")
    print("Task: " + task)
    shortcut = shortcutter_model.generate(task).model_dump()["parsed"]["shortcut"]
    print(shortcut)
    press_shortcut(shortcut)
    return {"result": "Done"}
