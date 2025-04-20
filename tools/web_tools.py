import webbrowser
import urllib.parse

def open_url(url: str) -> dict:
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
        return {"result": f"Successfully opened URL: {url}"}
    except Exception as e:
        print(f"Error opening URL '{url}': {e}")
        return {"error": f"Error opening URL '{url}': {e}"}


def search_web(query: str) -> dict:
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
        return {"result": f"Opened web search for: {query}"}
    except Exception as e:
        print(f"Error performing web search for '{query}': {e}")
        return {"error": f"Error performing web search for '{query}': {e}"}