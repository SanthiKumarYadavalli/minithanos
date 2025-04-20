import pyautogui as pg
import subprocess
from time import sleep


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
        subprocess.run("spotify")
        sleep(5)
        pg.hotkey("ctrl", "k")
        pg.write(song_name)
        sleep(4)
        pg.hotkey("shift", "enter")
        pg.press("esc")
        return {"message": "Done"}
    except Exception as e:
        print(f"Error playing song '{song_name}': {e}")
        return {"error": f"Error playing song '{song_name}': {e}"}


def control_music(action: str, volume_times: int) -> dict:
    """
    Controls music playback (play/pause, next, previous) or volume (up, down)
    by simulating media key presses..

    Args:
        action: The control action to perform. Valid actions are:
                "playpause", "nexttrack", "prevtrack", "volumeup", "volumedown".
        volume_times: The number of times to adjust the volume (for volume actions).

    Returns:
        A dictionary with the result or error of the action.
    """
    try:
        if action in ["volumeup", "volumedown"]:
            for _ in range(volume_times):
                pg.press(action)
        else:
            pg.press(action)
        return {"result": f"Successfully performed action: {action}"}
    except Exception as e:
        error_msg = f"Error performing action '{action}': {e}"
        return {"error": error_msg}
