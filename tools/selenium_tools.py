import google.ai.generativelanguage as glm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from gemini.web_model import get_xpath
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.parse import urljoin
import pyautogui as pg


driver = None
last_clicked_xpath = None

key_map = {
    "enter": Keys.ENTER, "tab": Keys.TAB, "backspace": Keys.BACKSPACE,
    "space": Keys.SPACE, "esc": Keys.ESCAPE, "delete": Keys.DELETE,
    "insert": Keys.INSERT, "arrow_up": Keys.ARROW_UP, "arrow_down": Keys.ARROW_DOWN,
    "arrow_left": Keys.ARROW_LEFT, "arrow_right": Keys.ARROW_RIGHT, "f1": Keys.F1,
    "f2": Keys.F2, "f3": Keys.F3, "f4": Keys.F4, "f5": Keys.F5, "f6": Keys.F6,
    "f7": Keys.F7, "f8": Keys.F8, "f9": Keys.F9, "f10": Keys.F10, "f11": Keys.F11,
    "f12": Keys.F12, "shift": Keys.SHIFT, "ctrl": Keys.CONTROL, "alt": Keys.ALT,
    "meta": Keys.META, "numpad_0": Keys.NUMPAD0, "numpad_1": Keys.NUMPAD1,
    "numpad_2": Keys.NUMPAD2, "numpad_3": Keys.NUMPAD3, "numpad_4": Keys.NUMPAD4,
    "numpad_5": Keys.NUMPAD5, "numpad_6": Keys.NUMPAD6, "numpad_7": Keys.NUMPAD7,
    "numpad_8": Keys.NUMPAD8, "numpad_9": Keys.NUMPAD9, "numpad_add": Keys.ADD,
    "numpad_subtract": Keys.SUBTRACT, "numpad_multiply": Keys.MULTIPLY,
    "numpad_divide": Keys.DIVIDE, "numpad_decimal": Keys.DECIMAL, "home": Keys.HOME,
    "end": Keys.END, "page_up": Keys.PAGE_UP, "page_down": Keys.PAGE_DOWN,
    "pause": Keys.PAUSE,
}



def launch_browser() -> dict:
    """
    Starts a new Chrome browser session using Selenium WebDriver if one is not already running.
    This function must be called before any other browser interaction functions.
    It maximizes the browser window upon launch. Subsequent calls do nothing if a browser is active.

    Returns:
        dict: A dictionary confirming the browser is launched or already running.
    """
    global driver
    if driver is None:
        print("INFO: Launching new Chrome browser...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # Consider adding options like --headless if you don't need to see the browser
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu") # Often needed with headless
        # options.add_argument("--window-size=1920,1080") # Set size for headless
        try:
            driver = webdriver.Chrome(service=Service(
                ChromeDriverManager().install()), options=options)
            print("INFO: Browser launched successfully.")
            return {"result": "Browser launched successfully."}
        except Exception as e:
            print(f"ERROR: Failed to launch browser: {e}")
            return {"error": f"Failed to launch browser: {e}"}
    else:
        print("INFO: Browser already running.")
        return {"result": "Browser already running."}


def navigate_current_tab(url: str) -> dict:
    """
    Navigates the currently active browser tab to the specified web address (URL).
    Requires the browser to be launched first via 'launch_browser'.
    The URL must be a complete web address, including 'http://' or 'https://'.

    Args:
        url (str): The full URL to load in the current tab.

    Returns:
        dict: A dictionary confirming navigation or reporting an error.
    """
    global driver
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    try:
        print(f"INFO: Navigating current tab to: {url}")
        driver.get(url)
        print(f"INFO: Navigation complete for {url}")
        return {"result": f"Successfully navigated to {url}"}
    except Exception as e:
        print(f"ERROR: Failed to navigate to {url}: {e}")
        return {"error": f"Failed to navigate to {url}: {e}"}


def open_url_in_new_tab(url: str) -> dict:
    """
    Opens a new browser tab, automatically switches focus to this new tab,
    and then navigates it to the specified URL.
    Requires the browser to be launched first. The URL must be complete.
    The URL must be a complete web address, including 'http://' or 'https://'.

    Args:
        url (str): The full URL to open in the new tab.

    Returns:
        dict: A dictionary confirming the action or reporting an error.
    """
    global driver
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    try:
        print(f"INFO: Opening URL in new tab: {url}")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        print(f"INFO: Opened and navigated new tab to: {url}")
        return {"result": f"Opened new tab and navigated to {url}"}
    except Exception as e:
        print(f"ERROR: Failed to open URL in new tab: {e}")
        return {"error": f"Failed to open URL in new tab: {e}"}


def switch_to_tab(index: int) -> dict:
    """
    Changes the browser's active focus to a specific tab, identified by its position.
    Tabs are indexed starting from 1 (the leftmost tab is 1, the next is 2, etc.).
    Use this before actions like clicking or typing if you need to target a non-active tab.
    Requires the browser to be launched.

    Args:
        index (int): The 1-based index of the target browser tab.

    Returns:
        dict: A dictionary confirming the switch or reporting an error.
    """
    global driver
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    try:
        tab_index = index - 1 # Convert 1-based to 0-based for list access
        if 0 <= tab_index < len(driver.window_handles):
            driver.switch_to.window(driver.window_handles[tab_index])
            print(f"INFO: Switched focus to tab {index}: {driver.current_url}")
            return {"result": f"Switched to tab {index}"}
        else:
            print(f"ERROR: Invalid tab index: {index}. Available tabs: {len(driver.window_handles)}")
            return {"error": f"Invalid tab index: {index}. Only {len(driver.window_handles)} tabs available."}
    except Exception as e:
        print(f"ERROR: Failed to switch tabs: {e}")
        return {"error": f"Failed to switch tabs: {e}"}


def close_current_tab() -> dict:
    """
    Closes the browser tab that is currently active.
    If other tabs remain open, focus automatically shifts to the last tab in the list.
    If it's the last tab, this might close the browser (behavior depends on browser/OS).
    Requires the browser to be launched.

    Returns:
        dict: A dictionary confirming the tab closure.
    """
    global driver
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    try:
        print("INFO: Closing current tab...")
        current_handles = len(driver.window_handles)
        driver.close()
        # Wait briefly to allow focus to shift if needed
        sleep(0.5)
        if len(driver.window_handles) < current_handles:
             if driver.window_handles:
                 # Switch to the last tab if any remain
                 driver.switch_to.window(driver.window_handles[-1])
                 print(f"INFO: Closed tab. Switched focus to last tab: {driver.current_url}")
             else:
                 print("INFO: Closed the last tab. Browser might be closed now.")
                 # driver = None # Optionally reset driver state if last tab closed the browser
             return {"result": "Current tab closed successfully."}
        else:
             # This case might happen if closing was blocked (e.g., by an alert)
             print("WARN: Tab close command issued, but tab count didn't decrease.")
             return {"result": "Attempted to close tab, but it might still be open."}

    except Exception as e:
        # Catching NoSuchWindowException if the window is already gone
        if "NoSuchWindowException" in str(type(e)):
             print("INFO: Current tab/window already closed.")
             if driver.window_handles:
                 driver.switch_to.window(driver.window_handles[-1])
                 print(f"INFO: Switched focus to last tab: {driver.current_url}")
                 return {"result": "Current tab was already closed. Focus moved."}
             else:
                 print("INFO: Browser already closed.")
                 # driver = None # Reset state
                 return {"result": "Browser was already closed."}
        else:
            print(f"ERROR: Failed to close tab: {e}")
            return {"error": f"Failed to close tab: {e}"}


def scroll_page(direction: str, amount: int) -> dict:
    """
    Scrolls the content of the currently active browser tab vertically.
    Requires the browser to be launched and a page loaded.

    Args:
        direction (str): The direction to scroll. Must be 'up' or 'down'.
        amount (int): The number of pixels to scroll. Must be a positive integer.

    Returns:
        dict: A dictionary confirming the scroll action or reporting an error.
    """
    global driver
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    if direction not in ["up", "down"]:
        return {"error": "Invalid scroll direction. Use 'up' or 'down'."}
    if not isinstance(amount, int) or amount <= 0:
        return {"error": "Invalid scroll amount. Must be a positive integer."}

    try:
        scroll_value = amount if direction == "down" else -amount
        driver.execute_script(f"window.scrollBy(0, {scroll_value});")
        print(f"INFO: Scrolled {direction} by {amount} pixels")
        return {"result": f"Scrolled {direction} by {amount} pixels."}
    except Exception as e:
        print(f"ERROR: Failed to scroll: {e}")
        return {"error": f"Failed to scroll: {e}"}


def perform_web_search(search_query: str) -> dict:
    """
    Attempts a web search using OS-level keyboard simulation (PyAutoGUI).
    It simulates pressing 'Ctrl+K' (common browser shortcut for address/search bar),
    types the query, and presses 'Enter'.
    Requires the browser window to be potentially active/focused on the OS level.

    Args:
        search_query (str): The text to search for on the web.

    Returns:
        dict: A dictionary confirming the action or reporting an error.
    """
    global driver
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    try:
        print(f"INFO: Performing OS-level web search for: '{search_query}'")
        sleep(1) # Allow brief moment for focus
        pg.hotkey("ctrl", "k") # Focus address/search bar
        sleep(0.5)
        pg.write(search_query, interval=0.05) # Type with slight delay
        sleep(0.5)
        pg.press("enter")
        print(f"INFO: OS-level search initiated for '{search_query}'")
        return {"result": f"OS-level search initiated for '{search_query}'."}
    except Exception as e:
        print(f"ERROR: Failed to perform OS-level web search: {e}")
        return {"error": f"Failed to perform OS-level web search: {e}"}


def type_text_into_element(text: str) -> dict:
    """
    Types the given text into the HTML input element that was most recently targeted
    by a successful 'click_element_by_description' call.
    **Crucially, this function depends on 'click_element_by_description' being called
    immediately prior on an input field or textarea.** It first clears the target field.
    Requires the browser to be launched.

    Args:
        text (str): The text content to type into the previously focused input field.

    Returns:
        dict: A dictionary confirming the typing action or reporting an error.
    """
    global driver, last_clicked_xpath
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}
    if last_clicked_xpath is None:
        return {"error": "No element recently targeted by 'click_element_by_description'. Cannot type."}

    try:
        print(f"INFO: Attempting to type '{text}' into element: {last_clicked_xpath}")
        element = driver.find_element("xpath", last_clicked_xpath)

        # Check if it's an input or textarea before clearing/typing
        if element.tag_name.lower() not in ['input', 'textarea']:
             print(f"WARN: Element {last_clicked_xpath} is not an input or textarea ({element.tag_name}). Typing might fail.")
             # Decide if you want to proceed or return an error here
             # return {"error": f"Targeted element '{last_clicked_xpath}' is not a text input field."}

        element.clear()
        sleep(0.2) # Small pause after clear
        # Simulate typing character by character for better realism if needed
        # for char in text:
        #    element.send_keys(char)
        #    sleep(0.03)
        element.send_keys(text)
        print(f"INFO: Successfully typed '{text}' into element: {last_clicked_xpath}")
        # Reset last_clicked_xpath after typing? Optional, depends on workflow.
        # last_clicked_xpath = None
        return {"result": f"Successfully typed '{text}'."}
    except Exception as e:
        print(f"ERROR: Failed to type into element {last_clicked_xpath}: {e}")
        # Reset last_clicked_xpath on error?
        # last_clicked_xpath = None
        return {"error": f"Failed to type into element {last_clicked_xpath}: {e}"}


def click_element_by_description(description: str) -> dict:
    """
    Finds an interactive element (button, link, input field, etc.) on the current webpage
    based on a natural language description provided by the user. It uses an external helper
    function (`get_xpath`) which analyzes the page's HTML (specifically the <body> content)
    to determine the most likely XPath for the described element.

    **Behavior:**
    1. Retrieves the current page's HTML body.
    2. Calls `get_xpath` with the HTML and the `description`.
    3. If `get_xpath` returns a valid XPath:
        a. **Stores this XPath globally** for potential use by `type_text_into_element`.
        b. Checks if the XPath identifies a link (`<a>` tag with an `href` attribute).
        c. **If it's a link:** It extracts the URL (`href`). If the URL is relative (starts with '/'), it converts it to an absolute URL based on the current page's address. Then, it **navigates the current tab** to this URL using the `navigate_current_tab` function's logic.
        d. **If it's not a link:** It finds the element using the XPath and performs a standard Selenium click action on it.
    4. If `get_xpath` fails or returns an invalid XPath, an error is reported.

    **Use this function to:** Interact with elements when you can describe them (e.g., "click the 'Submit' button", "find the search input field", "click the link named 'Privacy Policy'").

    **Important:** The success depends heavily on the quality of the `description` and the ability of the external `get_xpath` function to correctly identify the element on the current page structure. The found element's XPath is saved, overwriting any previously saved XPath.

    Args:
        description (str): A natural language phrase describing the element to click.
                           Examples: 'the login button', 'search input field',
                           'the link with text Read More', 'the checkbox for newsletter'.

    Returns:
        dict: A dictionary confirming the click/navigation action or reporting an error.
    """
    global driver, last_clicked_xpath
    if driver is None:
        return {"error": "Browser not launched. Call 'launch_browser' first."}

    try:
        print(f"INFO: Attempting to find element described as: '{description}'")
        # 1. Get HTML
        try:
            body_element = driver.find_element("tag name", "body")
            current_html = body_element.get_attribute("outerHTML")
        except Exception as e:
            print(f"ERROR: Could not get page HTML: {e}")
            return {"error": f"Could not get page HTML: {e}"}

        # 2. Call external function to get XPath
        try:
            # Assuming get_xpath returns a dictionary like {"xpath": "..."} or raises error
            xpath_response = get_xpath(current_html, description)
            if "xpath" not in xpath_response or not xpath_response["xpath"]:
                 print(f"ERROR: get_xpath did not return a valid XPath for '{description}'. Response: {xpath_response}")
                 return {"error": f"Could not determine XPath for description: '{description}'."}
            xpath = xpath_response["xpath"]
        except Exception as e:
            print(f"ERROR: Call to get_xpath failed for '{description}': {e}")
            return {"error": f"Failed to get XPath using description '{description}': {e}"}

        print(f"INFO: Extracted XPath: {xpath}")
        # 3a. Store XPath globally
        last_clicked_xpath = xpath

        # 3b & 3c. Check if it's a link and navigate
        # A simple check: does xpath likely select an 'a' tag AND contain '@href'? More robust checks possible.
        is_link_xpath = ("//a" in xpath or "/a[" in xpath) and "@href" in xpath
        if is_link_xpath:
             # Try finding the element first to extract href reliably
             try:
                 link_element = driver.find_element("xpath", xpath)
                 href = link_element.get_attribute('href')
                 if href:
                     print(f"INFO: XPath identifies a link. Extracted href: {href}")
                     # Handle relative URLs
                     if href.startswith("/"):
                         base_url = "/".join(driver.current_url.split("/", 3)[:3])
                         absolute_url = urljoin(base_url, href)
                         print(f"INFO: Converted relative URL to absolute: {absolute_url}")
                     elif href.startswith("http://") or href.startswith("https://"):
                         absolute_url = href
                     elif href.startswith("javascript:"):
                         print(f"INFO: Link has javascript href ('{href}'). Attempting standard click instead of navigation.")
                         # Fallback to standard click for javascript links
                         link_element.click()
                         sleep(1) # Wait after click
                         print(f"INFO: Clicked javascript link described as '{description}'")
                         return {"result": f"Clicked javascript link described as '{description}'."}
                     else: # Handle other cases like mailto: or relative paths without leading / if needed
                         print(f"WARN: Unhandled link type or relative path: {href}. Attempting standard click.")
                         link_element.click() # Try clicking anyway
                         sleep(1)
                         print(f"INFO: Clicked element described as '{description}' (non-standard link).")
                         return {"result": f"Clicked non-standard link described as '{description}'."}

                     # Navigate if we have a valid absolute http/https URL
                     print(f"INFO: Navigating to link URL: {absolute_url}")
                     driver.get(absolute_url)
                     sleep(2) # Wait for page load
                     print(f"INFO: Navigation to link complete.")
                     return {"result": f"Navigated to link URL from description '{description}'."}
                 else:
                    print(f"WARN: Link element found but has no href attribute. Attempting standard click.")
                    # Fallback to standard click if href is missing
                    link_element.click()
                    sleep(1)
                    print(f"INFO: Clicked element described as '{description}' (link without href).")
                    return {"result": f"Clicked element described as '{description}' (link without href)."}

             except Exception as e:
                 print(f"ERROR: Failed to process link element {xpath}: {e}")
                 return {"error": f"Failed to process link element described as '{description}': {e}"}
        else:
            # 3d. Perform standard click
            print(f"INFO: Element is not a standard link. Performing standard click.")
            element_obj = driver.find_element("xpath", xpath)
            # Optional: Scroll into view before clicking
            # driver.execute_script("arguments[0].scrollIntoView(true);", element_obj)
            # sleep(0.5)
            element_obj.click()
            sleep(1) # Wait a moment after click for potential page changes
            print(f"INFO: Clicked element described as '{description}'")
            return {"result": f"Clicked element described as '{description}'."}

    except Exception as e:
        # Catch potential NoSuchElementException here too
        if "NoSuchElementException" in str(type(e)):
             print(f"ERROR: Element described as '{description}' not found on page with XPath {last_clicked_xpath}.")
             last_clicked_xpath = None # Reset if not found
             return {"error": f"Element described as '{description}' not found on page."}
        else:
            print(f"ERROR: Failed to click element described as '{description}': {e}")
            # Consider resetting last_clicked_xpath on generic errors too
            # last_clicked_xpath = None
            return {"error": f"Failed to click element described as '{description}': {e}"}


def close_browser() -> dict:
    """
    Closes all browser windows and tabs associated with the current WebDriver session,
    effectively ending the automation task. Call this function when all browser
    operations are complete.

    Returns:
        dict: A dictionary confirming the browser closure.
    """
    global driver, last_clicked_xpath
    if driver:
        try:
            print("INFO: Closing browser...")
            driver.quit()
            driver = None
            last_clicked_xpath = None # Clear state on exit
            print("INFO: Browser closed successfully.")
            return {"result": "Browser closed successfully."}
        except Exception as e:
            print(f"ERROR: Error closing browser: {e}")
            # Attempt to force reset state even if quit fails
            driver = None
            last_clicked_xpath = None
            return {"error": f"Error closing browser: {e}"}
    else:
        print("INFO: Browser already closed.")
        return {"result": "Browser was already closed."}






