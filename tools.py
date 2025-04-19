from agents.coder import generate_and_write_code
from agents.shortcutter import perform_shortcut
from agents.spotify import play_song
from agents.commander import run_command
from agents.watcher import look_at_my_screen
from utils import write_text
import pyautogui as pg
import webbrowser
import os
import pyperclip
import datetime
import urllib.parse


def press_key(key: str):
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
        return f"Successfully pressed key: {key}"
    except Exception as e:
        print(f"Error pressing key '{key}': {e}")
        return f"Error pressing key '{key}': {e}"
    

def close_tab():
    """
    Closes the currently active tab in a web browser using Ctrl+W (Windows/Linux)
    or Cmd+W (macOS). Adapt if needed.
    """
    print("Action: Attempting to close active tab...")
    pg.hotkey('ctrl', 'w')
    print("Action completed: Close tab command sent.")
    return "Done"


def close_window():
    """
    Closes the currently active window using Alt+F4 (Windows/Linux)
    or Cmd+W (macOS). Adapt if needed.
    """
    print("Action: Attempting to close active window...")
    # Simple platform check (can be improved)
    pg.hotkey('alt', 'f4')
    print("Action completed: Close window command sent.")
    return "closed window"


def take_screenshot() -> str:
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
        return f"Screenshot saved to {abs_path}"
    except Exception as e:
        print(f"Error taking screenshot: {e}")
        return f"Error taking screenshot: {e}"

# --- Web Interaction Tools ---

def open_url(url: str):
    """
    Opens the given URL in the default web browser.

    Args:
        url: The URL to open (should include http:// or https://).
    """
    try:
        # Basic validation/correction
        if not url.startswith(('http://', 'https://')):
            print(f"Info: Adding https:// to URL '{url}'")
            url = 'https://' + url

        print(f"Action: Opening URL: '{url}'")
        webbrowser.open(url)
        print("Action completed: URL opened in browser.")
        return f"Successfully opened URL: {url}"
    except Exception as e:
        print(f"Error opening URL '{url}': {e}")
        return f"Error opening URL '{url}': {e}"


def search_web(query: str):
    """
    Performs a web search using the default browser and Google.

    Args:
        query: The search term(s).
    """
    try:
        print(f"Action: Searching web for: '{query}'")
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(search_url)
        print("Action completed: Web search opened in browser.")
        return f"Opened web search for: {query}"
    except Exception as e:
        print(f"Error performing web search for '{query}': {e}")
        return f"Error performing web search for '{query}': {e}"


def get_clipboard_text() -> str:
    """
    Gets the current text content from the system clipboard.

    Returns:
        The text from the clipboard or an error message.
    """

    print("Action: Getting clipboard text.")
    text = pyperclip.paste()
    print(f"Action completed: Retrieved {len(text)} characters from clipboard.")
    return text if text else "Clipboard is empty or contains non-text data."


def set_clipboard_text(text: str):
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
        return "Successfully copied text to clipboard."
    except Exception as e:
        print(f"Error setting clipboard content: {e}")
        return f"Error setting clipboard: {e}"


# --- Utility Tools ---
def get_current_datetime() -> str:
    """
    Gets the current date and time.

    Returns:
        A string representing the current date and time.
    """
    print("Action: Getting current date and time.")
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return f"The current date and time is: {formatted_time}"


def open_apps(app_name: str) -> str:
    """
    
    Opens the specified application by name.

    Args:
        app_name: The name of the application to open.

    Returns:
        A success message or an error message.
    """
    try:
        print(f"Action: Opening application: '{app_name}'")
        pg.press("win")
        pg.write(app_name)
        pg.press("enter")
        return f"Successfully opened application: {app_name}"
    except Exception as e:
        print(f"Error opening application '{app_name}': {e}")
        return f"Error opening application '{app_name}': {e}"


FUNCTIONS = {
    "generate_and_write_code": generate_and_write_code,
    "run_command": run_command,
    "perform_shortcut": perform_shortcut,
    "play_song": play_song,
    "write_text": write_text,
    "look_at_my_screen": look_at_my_screen,
    "press_key": press_key,
    "close_window": close_window,
    "take_screenshot": take_screenshot,
    "open_url": open_url,
    "search_web": search_web,
    "get_clipboard_text": get_clipboard_text,
    "set_clipboard_text": set_clipboard_text,
    "get_current_datetime": get_current_datetime,
    "open_apps": open_apps
}
