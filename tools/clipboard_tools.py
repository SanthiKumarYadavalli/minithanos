import pyperclip
import pyautogui as pg


def get_clipboard_text() -> dict:
    """
    Gets the current text content from the system clipboard.

    Returns:
        The text from the clipboard or an error message.
    """
    print("Action: Getting clipboard text.")
    text = pyperclip.paste()
    print(f"Action completed: Retrieved {len(text)} characters from clipboard.")
    return {"result": text if text else "Clipboard is empty or contains non-text data."}


def set_clipboard_text(text: str) -> dict:
    """
    Sets the system clipboard text content.

    Args:
        text: The text to place on the clipboard.

    Returns:
        A success message or an error message.
    """
    try:
        print(f"Action: Setting clipboard text: '{text[:50]}...'")
        pyperclip.copy(text)
        print("Action completed: Text copied to clipboard.")
        return {"result": "Successfully copied text to clipboard."}
    except Exception as e:
        print(f"Error setting clipboard content: {e}")
        return {"error": f"Error setting clipboard: {e}"}


def get_selected_text():
    """
    Copy the selected text, get it from the clipboard.

    Returns:
        str: The selected text from the clipboard.
    """
    pg.hotkey('ctrl', 'c')
    selected_text = pyperclip.paste()
    return selected_text