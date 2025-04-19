from google.genai import types
from .client import client

def generate():
    model = "gemini-1.5-flash"
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    
    file = client.files.upload(file="screenshot.png")
    return client.models.generate_content(
        model=model,
        contents=["Describe what's on my screen.", file],
        config=generate_content_config,
    )

if __name__ == "__main__":
    generate()