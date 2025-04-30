from tools.selenium_tools import *
from google.genai import types

launch_browser_declaration = types.FunctionDeclaration(
    name="launch_browser",
    description="Starts a new Chrome browser session using Selenium WebDriver if one is not already running. Maximizes the window. Must be called before other browser actions.",
)

navigate_current_tab_declaration = types.FunctionDeclaration(
    name="navigate_current_tab",
    description="Navigates the currently active browser tab to the specified web address (URL). Requires the browser to be launched. URL must be complete (e.g., 'https://www.google.com').",
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'url': types.Schema(
                type='STRING',
                description="The full URL to load in the current tab."
            )
        },
        required=['url'],
    ),
)

open_url_in_new_tab_declaration = types.FunctionDeclaration(
    name="open_url_in_new_tab",
    description="Opens a new browser tab, switches focus to it, and navigates it to the specified URL. Requires the browser to be launched. URL must be complete.",
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'url': types.Schema(
                type='STRING',
                description="The full URL to open in the new tab."
            )
        },
        required=['url'],
    ),
)

switch_to_tab_declaration = types.FunctionDeclaration(
    name="switch_to_tab",
    description="Changes the active browser focus to a specific tab using its 1-based index (1=leftmost). Required before acting on a non-active tab.",
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'index': types.Schema(
                type='INTEGER',
                description="The 1-based index of the tab to switch focus to."
            )
        },
        required=['index'],
    ),
)

close_current_tab_declaration = types.FunctionDeclaration(
    name="close_current_tab",
    description="Closes the currently active browser tab. Focus automatically shifts to the last remaining tab if any.",
)

scroll_page_declaration = types.FunctionDeclaration(
    name="scroll_page",
    description="Scrolls the content of the currently active browser tab vertically up or down.",
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'direction': types.Schema(
                type='STRING',
                description="Direction to scroll. Must be 'up' or 'down'."
            ),
            'amount': types.Schema(
                type='INTEGER',
                description="Positive integer number of pixels to scroll."
            )
        },
        required=['direction', 'amount'],
    ),
)

perform_web_search_declaration = types.FunctionDeclaration(
    name="perform_web_search",
    description="Fallback web search using OS-level keyboard simulation (Ctrl+K, type, Enter). Less reliable than specific element interaction. Use if direct search input interaction fails.",
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'search_query': types.Schema(
                type='STRING',
                description="The text to search for on the web."
            )
        },
        required=['search_query'],
    ),
)

type_text_into_element_declaration = types.FunctionDeclaration(
    name="type_text_into_element",
    description="Types text into the input field or textarea that was the target of the *immediately preceding* successful 'click_element_by_description' call. Clears the field first. Fails if 'click_element_by_description' wasn't just called on an input.",
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'text': types.Schema(
                type='STRING',
                description="The text to type into the previously focused element."
            )
        },
        required=['text'],
    ),
)

click_element_by_description_declaration = types.FunctionDeclaration(
    name="click_element_by_description",
    description=(
        "Finds and interacts with an element on the current page based on a natural language 'description'. "
        "Uses an external AI helper (`get_xpath`) to find the element's XPath from the page HTML. "
        "IMPORTANT BEHAVIOR: If the described element is a standard web link (<a> tag with an 'href' pointing to http/https), this function will **navigate** the current tab to that link's URL. "
        "If the element is anything else (button, input field, checkbox, non-navigable link like javascript:), it performs a standard **click** action. "
        "If the clicked element is an input field or textarea, its XPath is stored internally, allowing the *next* action to be 'type_text_into_element'. "
        "Use descriptive text like 'the button labeled Submit', 'the search bar', 'the link Read More', 'the checkbox for terms and conditions'."
    ),
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'description': types.Schema(
                type='STRING',
                description="Natural language description of the element to click or navigate from (e.g., 'the login button', 'search input field', 'link named About Us')."
            )
        },
        required=['description'],
    ),
)

close_browser_declaration = types.FunctionDeclaration(
    name="close_browser",
    description="Closes all browser windows and tabs, terminating the WebDriver session. Call this when all automation tasks are finished.",
)

SELENIUM_TOOLS = types.Tool(
    function_declarations=[
        launch_browser_declaration,
        navigate_current_tab_declaration,
        open_url_in_new_tab_declaration,
        switch_to_tab_declaration,
        close_current_tab_declaration,
        scroll_page_declaration,
        perform_web_search_declaration,
        type_text_into_element_declaration,
        click_element_by_description_declaration,
        close_browser_declaration,
    ], 
)

SELENIUM_FUNCTION_MAP = {
    "launch_browser": launch_browser,
    "navigate_current_tab": navigate_current_tab,
    "open_url_in_new_tab": open_url_in_new_tab,
    "switch_to_tab": switch_to_tab,
    "close_current_tab": close_current_tab,
    "scroll_page": scroll_page,
    "perform_web_search": perform_web_search,
    "type_text_into_element": type_text_into_element,
    "click_element_by_description": click_element_by_description,
    "close_browser": close_browser,
}