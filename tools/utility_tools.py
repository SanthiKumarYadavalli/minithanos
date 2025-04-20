import pyautogui as pg
import datetime
import os
from utils import run_command, update_files_list

def get_current_datetime() -> dict:
    """
    Gets the current date and time.

    Returns:
        A string representing the current date and time.
    """
    print("Action: Getting current date and time.")
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return {"result": f"The current date and time is: {formatted_time}"}


def open_apps(app_name: str) -> dict:
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
        return {"result": f"Successfully opened application: {app_name}"}
    except Exception as e:
        print(f"Error opening application '{app_name}': {e}")
        return {"error": f"Error opening application '{app_name}': {e}"}


def open_file(file_path: str) -> dict:
    """
    Opens a file using the default application associated with its file type.

    Args:
        file_path: The path to the file to open.

    Returns:
        A success message or an error message.
    """
    try:
        
        print(f"Action: Opening file: '{file_path}'")
        update_files_list()
        run_command(f"start {file_path}")
        return {"result": f"Successfully opened file: {file_path}"}
    except Exception as e:
        print(f"Error opening file '{file_path}': {e}")
        return {"error": f"Error opening file '{file_path}': {e}"}


def open_folder(folder_path: str) -> dict:
    """
    Opens a folder in the file explorer.

    Args:
        folder_path: The path to the folder to open.

    Returns:
        A success message or an error message.
    """
    try:
        print(f"Action: Opening folder: '{folder_path}'")
        run_command(f"start {folder_path}")
        return {"result": f"Successfully opened folder: {folder_path}"}
    except Exception as e:
        print(f"Error opening folder '{folder_path}': {e}")
        return {"error": f"Error opening folder '{folder_path}': {e}"}


def execute_command(command: str) -> dict:
    """
    Perform OS related tasks by running a command.
    Use bash commands for this.
    Technical Constraints:
    *   Shell: Target `bash` on Linux.
    *   File/Directory Names: Assume names may contain SPACES. Use proper quoting (e.g., double quotes `""`) to handle them correctly.
    *   Wildcards: Use wildcards outside quotes for file matching (globbing), e.g., `rm *.tmp`, `mv "target dir/"?.txt ./`. Avoid constructs like `rm "*.tmp"`.
    Args:
        command(str): the command to execute
    """
    output = run_command(command)
    print(command, output)
    return {"output": output.get("output"), "error": output.get("error")}