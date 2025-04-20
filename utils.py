import pyautogui as pg
import pyperclip
import subprocess


def write_code(code: str) -> dict:
    """
    types the given code into the active text field
    Args:
        code (str): the code to type
    """
    for line in code.split("\n"):
        pg.hotkey("home")
        pyperclip.copy(line)
        pg.hotkey("ctrl", "v")
        pg.press("enter")
    return {"message": "done"}


def write_text(text: str) -> dict:
    """
    types the given text into the active text field
    Args:
        text (str): the text to type
    """
    print("WRITER called!")
    pyperclip.copy(text)
    pg.hotkey("ctrl", "v")
    pg.press("enter")
    return {"message": "done"}


def press_shortcut(shortcut):
    pg.hotkey(*shortcut)
    
    
def update_files_list():
    directories = [
        "~/Desktop",
        "~/Downloads",
        "~/Documents",
        "~/Videos",
        "~/Pictures",
        "~/Music",
    ]
    skip_files = [
        "*/.git/*",
        "*/.vscode/*",
        "*/__pycache__/*",
        "*/node_modules/*",
        "*/venv/*",
    ]
    subprocess.run([
        "find",
        *directories, 
        "-type", "f",
        *(x for file in skip_files for x in ("-not", "-path", f"\"{file}\"")), 
        ">", "files.txt"
    ], shell=True)


def get_files_list():
    result = subprocess.run([
        "cat",
        "files.txt"
    ], shell=True, capture_output=True, text=True)
    return result.stdout


def run_command(command):
    output = subprocess.run([r"C:\Program Files\Git\bin\bash.exe", "-c", command], shell=True, capture_output=True)
    return {"output": output.stdout.decode("utf-8"), "error": output.stderr.decode("utf-8")}


def take_screenshot():
    pg.screenshot("screenshot.png")