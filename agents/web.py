from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from gemini.web_model import get_xpath, get_summarize_text
from selenium.webdriver.common.keys import Keys

key_map = {
    "enter": Keys.ENTER,
    "tab": Keys.TAB,
    "backspace": Keys.BACKSPACE,
    "space": Keys.SPACE,
    "esc": Keys.ESCAPE,
    "delete": Keys.DELETE,
    "insert": Keys.INSERT,

    # Arrow Keys
    "arrow_up": Keys.ARROW_UP,
    "arrow_down": Keys.ARROW_DOWN,
    "arrow_left": Keys.ARROW_LEFT,
    "arrow_right": Keys.ARROW_RIGHT,

    # Function Keys (F1-F12)
    "f1": Keys.F1,
    "f2": Keys.F2,
    "f3": Keys.F3,
    "f4": Keys.F4,
    "f5": Keys.F5,
    "f6": Keys.F6,
    "f7": Keys.F7,
    "f8": Keys.F8,
    "f9": Keys.F9,
    "f10": Keys.F10,
    "f11": Keys.F11,
    "f12": Keys.F12,

    # Modifier Keys
    "shift": Keys.SHIFT,
    "ctrl": Keys.CONTROL,
    "alt": Keys.ALT,
    "meta": Keys.META,   # Windows/Command key

    # Numeric Keypad
    "numpad_0": Keys.NUMPAD0,
    "numpad_1": Keys.NUMPAD1,
    "numpad_2": Keys.NUMPAD2,
    "numpad_3": Keys.NUMPAD3,
    "numpad_4": Keys.NUMPAD4,
    "numpad_5": Keys.NUMPAD5,
    "numpad_6": Keys.NUMPAD6,
    "numpad_7": Keys.NUMPAD7,
    "numpad_8": Keys.NUMPAD8,
    "numpad_9": Keys.NUMPAD9,
    "numpad_add": Keys.ADD,
    "numpad_subtract": Keys.SUBTRACT,
    "numpad_multiply": Keys.MULTIPLY,
    "numpad_divide": Keys.DIVIDE,
    "numpad_decimal": Keys.DECIMAL,

    # Special Keys
    "home": Keys.HOME,
    "end": Keys.END,
    "page_up": Keys.PAGE_UP,
    "page_down": Keys.PAGE_DOWN,
    "pause": Keys.PAUSE,
}


class BrowserCLI:
    def __init__(self):
        """Initialize WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)
        self.xpaths = []

        # Command mapping
        self.commands = {
            "open": self.open_website,
            "newtab": self.new_tab,
            "switch": self.switch_tab,
            "scroll": self.scroll,
            "close": self.close_tab,
            "exit": self.exit_browser,
            "press": self.press_key,
            "type": self.type_text,
            "click": self.click_element,
            "help": self.show_help,
            "summary": self.summarize_link,
        }

    def summarize_link(self):
        link = self.driver.current_url
        print(get_summarize_text(link))
        return

    def open_website(self, url):
        self.driver.get(url)
        print(f"Opened: {url}")

    def new_tab(self, url):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(url)
        print(f"Opened new tab: {url}")

    def switch_tab(self, index):
        try:
            self.driver.switch_to.window(
                self.driver.window_handles[int(index) - 1])
            print(f"Switched to tab {index}: {self.driver.current_url}")
        except (IndexError, ValueError):
            print(f"Invalid tab index: {index}")

    def close_tab(self):
        self.driver.close()
        if self.driver.window_handles:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        print("Closed current tab")

    def scroll(self, direction, amount):
        amount = int(amount)
        scroll_value = amount if direction == "down" else -amount
        self.driver.execute_script(f"window.scrollBy(0, {scroll_value});")
        print(f"Scrolled {direction} by {amount} pixels")

    def type_text(self, *text):
        try:
            element = self.driver.find_element("xpath", self.xpaths[-1])
            element.clear()
            element.send_keys(" ".join(text))
            print(f"Typed '{text}' into element: {element}")
        except Exception as e:
            print(f"Error typing into element: {e}")

    # def type_text(self, method, value, *text):
    #     """Type text into an input field using id, class, name, xpath, css"""

    #     text = " ".join(text)  # Combine multiple words
    #     try:
    #         element = self.driver.find_element(method, value)
    #         element.clear()
    #         element.send_keys(text)
    #         print(f"Typed '{text}' into [{method}='{value}']")
    #     except Exception as e:
    #         print(f"Error typing into [{method}='{value}']: {e}")

    def click_element(self, *element) -> None:
        try:
            element = " ".join(element)
            response = get_xpath(self.get_body_html(), element)
            xpath = response["xpath"]
            self.xpaths.append(xpath)
            print(f"Extracted XPath: {xpath}")
            element = self.driver.find_element("xpath", xpath)
            element.click()
            print(f"Clicked element: {element}")
        except Exception as e:
            print(f"Error clicking element: {e}")

    # def click_element(self, method, value):
    #     """Click an element using different methods (id, class, name, xpath)"""
    #     try:
    #         element = self.driver.find_element(method, value)
    #         element.click()
    #         print(f"Clicked element [{method}='{value}']")
    #     except Exception as e:
    #         print(f"Error clicking element [{method}='{value}']: {e}")

    def press_key(self, key):
        """Simulates pressing a keyboard key in the browser."""

        if key.lower() in key_map:
            webdriver.ActionChains(self.driver).send_keys(
                key_map[key.lower()]).perform()
            print(f"Pressed {key}")
        else:
            print(f"Key '{key}' is not mapped!")

    def get_body_html(self):
        """Returns the raw HTML of the page starting from the <body> tag."""
        body_element = self.driver.find_element(
            "tag name", "body")  # Locate <body> tag
        return body_element.get_attribute("outerHTML")  # Get its HTML content

    def exit_browser(self):
        self.driver.quit()
        print("Browser closed. Exiting CLI.")
        exit()

    def show_help(self):
        print("\nCommands:\n"
              "  open <url>          - Open a website in the current tab\n"
              "  newtab <url>        - Open a new tab with a website\n"
              "  click element  - Click an element\n"
              "  type <text> - Type text into an input field\n"
              "  switch <index>      - Switch to a tab (1-based index)\n"
              "  press <key>         - Press a keyboard key\n"
              "  scroll <up/down> <pixels> - Scroll up or down\n"
              "  summary             - Summarize the current page\n"
              "  close               - Close the current tab\n"
              "  exit                - Close browser and exit\n")

    def run(self):
        print("\n🚀 Browser Automation CLI started! Type 'help' for commands.")
        while True:
            cmd = input("\n>>> ").strip().split()
            if not cmd:
                continue

            action = cmd[0].lower()
            args = cmd[1:]

            if action in self.commands:
                try:
                    if args:
                        self.commands[action](*args)
                    else:
                        self.commands[action]()
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    BrowserCLI().run()
