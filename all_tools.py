from tools.gui_tools import press_key, close_tab, close_window, take_screenshot, press_shortcut
from tools.web_tools import open_url, search_web
from tools.clipboard_tools import get_clipboard_text, set_clipboard_text
from tools.utility_tools import get_current_datetime, open_apps, open_file, open_folder, execute_command
from tools.music_tools import play_song, control_music
from agents.watcher import look_at_my_screen
from utils import write_text, write_code

FUNCTIONS = {
    "press_key": press_key,
    "close_tab": close_tab,
    "close_window": close_window,
    "take_screenshot": take_screenshot,
    "press_shortcut": press_shortcut,
    "open_url": open_url,
    "search_web": search_web,
    "get_clipboard_text": get_clipboard_text,
    "set_clipboard_text": set_clipboard_text,
    "get_current_datetime": get_current_datetime,
    "open_apps": open_apps,
    "open_file": open_file,
    "open_folder": open_folder,
    "execute_command": execute_command,  
    "play_song": play_song,                   
    "write_text": write_text,
    "write_code": write_code,             
    "look_at_my_screen": look_at_my_screen,
    "control_music": control_music,    
}
