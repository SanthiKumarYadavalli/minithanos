import pyautogui as pg
import datetime
import os
import subprocess


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
    """
    print("Shortcut called", keys)
    pg.hotkey(*keys.split())
    return {"result": "done"}


def play_song(song_name: str) -> dict:
    """
    Plays a song using Spotify by simulating a search and play action.

    Args:
        song_name: The name of the song to play.

    Returns:
        A dictionary with the result of the action.
    """
    try:
        print(f"Action: Searching and playing song: '{song_name}'")
        # Simulate opening Spotify and searching for the song
        subprocess.run("spotify")
        pg.sleep(2)  # Wait for Spotify to open
        pg.hotkey('ctrl', 'l')  # Focus search bar
        pg.write(song_name)  # Type the song name
        pg.press("enter")  # Search for the song
        pg.sleep(1)  # Wait for search results
        pg.press("enter")  # Play the first result
        print(f"Action completed: Playing song '{song_name}'")
        return {"result": f"Playing song: {song_name}"}
    except Exception as e:
        print(f"Error playing song '{song_name}': {e}")
        return {"error": f"Error playing song '{song_name}': {e}"}