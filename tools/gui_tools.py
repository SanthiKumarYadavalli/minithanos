import pyautogui as pg
import datetime
import os


def press_key(key: str) -> dict:
    """
    Presses a single keyboard key.
    See pyautogui documentation for key names (e.g., 'enter', 'f1', 'ctrlleft').

    Args:
        key: The name of the key to press.
    """
    try:
        print(f"Action: Pressing key: '{key}'")
        pg.press(key)
        print(f"Action completed: Key '{key}' pressed.")
        return {"result": f"Successfully pressed key: {key}"}
    except Exception as e:
        print(f"Error pressing key '{key}': {e}")
        return {"error": f"Error pressing key '{key}': {e}"}
    

def close_tab() -> dict:
    """
    Closes the currently active tab in a web browser using Ctrl+W (Windows/Linux)
    or Cmd+W (macOS). Adapt if needed.
    """
    print("Action: Attempting to close active tab...")
    pg.hotkey('ctrl', 'w')
    print("Action completed: Close tab command sent.")
    return {"result": "Done"}


def close_window() -> dict:
    """
    Closes the currently active window using Alt+F4 (Windows/Linux)
    or Cmd+W (macOS). Adapt if needed.
    """
    print("Action: Attempting to close active window...")
    # Simple platform check (can be improved)
    pg.hotkey('alt', 'f4')
    print("Action completed: Close window command sent.")
    return {"result": "closed window"}


def take_screenshot() -> dict:
    """
    Takes a screenshot and saves it to a file.

    Args:
        filename: The path to save the screenshot. If None, generates a timestamped filename.

    Returns:
        The path where the screenshot was saved or an error message.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"C:/Users/santh/Desktop/screenshot_{timestamp}.png"
        print(f"Action: Taking screenshot and saving to '{filename}'")
        pg.screenshot(filename)
        abs_path = os.path.abspath(filename)
        print(f"Action completed: Screenshot saved to '{abs_path}'")
        return {"result": f"Screenshot saved to {abs_path}"}
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return {"error": f"Error taking screenshot: {e}"}



def press_shortcut(keys: str) -> dict:
    """
    presses hotkeys. for example pressing a shortcut.
    Args:
        keys(str): a space separated string of keys (pyautogui keys)
        example: "ctrl a" or "ctrl alt delete"
    """
    print("Shortcut called", keys)
    pg.hotkey(*keys.split())
    return {"result": "done"}


def send_message_or_text(text: str) -> dict:
    """
    Sends a message or types text into the active text field.
    This is useful for chat applications or any text input field.
    Args:
        text (str): the text to type
    """
    print("Action: Sending message or text.")
    pg.write(text, interval=0.1)  # Adjust interval for typing speed
    pg.press("enter")
    print(f"Action completed: Typed and sent '{text}'")
    return {"result": "done"}

