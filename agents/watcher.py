from gemini import watcher_model
from utils import write_text, take_screenshot


def look_at_my_screen() -> dict:
    """
    Describes my current screen.
    """
    take_screenshot()
    print("WATCHER CALLED!")
    description = watcher_model.generate().text
    print(description)
    return {"description": description}