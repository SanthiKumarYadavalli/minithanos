from gemini import shortcutter_model
from gui_utils import press_shortcut

def perform_shortcut(prompt: str) -> None:
    """
    Generate a shortcut for a given prompt and press it.
    Args:
        prompt (str): The prompt to generate a shortcut from.
    """
    shortcut = shortcutter_model.generate(prompt).model_dump()["parsed"]["shortcut"]
    press_shortcut(shortcut)
