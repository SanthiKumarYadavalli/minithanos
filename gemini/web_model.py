from google import genai
from google.genai import types
import json

client = genai.Client(api_key="AIzaSyAkSmvQGTAMQblIWJPT0ufPzr7vFLgmJog")


def get_summarize_text(link):
    model = "gemini-2.0-flash"
    config = types.GenerateContentConfig(
        response_mime_type='text/plain'
    )
    response = client.models.generate_content(
        model=model,
        contents=[f"Explain me about this page content: {link}\n"],
        config=config
    ).text
    return response


def get_xpath(rawHtml, element):
    model = "gemini-2.0-flash"
    config = types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'required': [
                'xpath'
            ],
            'properties': {
                'xpath': {'type': 'STRING', 'description': 'The exact XPath by only (href or id or text or unique identifier) of the specified UI element in the DOM.'},
            },
            'type': 'OBJECT',
            'description': 'Extracts the exact XPath by only (href or id or text or unique identifier) of a UI element based on the provided raw HTML and description.',
        })
    response = client.models.generate_content(
        model=model,
        contents=["I will give the raw html and 'the thing that use want to interact like(open first link in google search page) or input field name username like that or searchbar' give me exact the xpath by only (href or id or text or unique identifier)",
                  f"UI element: {element}\n", f"Raw html: {rawHtml}\n"],
        config=config
    ).text
    return json.loads(response)
