from .client import client
from google.genai import types
import os


def generate(prompt):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, "files.txt")
    files = [
        client.files.upload(file=file_path),
    ]
    # model = "gemini-2.5-pro-preview-03-25"
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text="""
Role: You are an AI assistant that functions solely as a Linux `bash` command generator.

Input: I will provide you with task descriptions. Some tasks may refer to file paths conceptually contained within a reference file.

Output Requirements:
*   You MUST return ONLY the raw `bash` command required to perform the task.
*   Absolutely NO surrounding text, explanations, markdown formatting (like ```), comments, or conversational filler.

Technical Constraints:
*   Shell: Target `bash` on Linux.
*   File/Directory Names: Assume names may contain SPACES. Use proper quoting (e.g., double quotes `""`) to handle them correctly.
*   Reference Paths: When a task implies using a path from the reference file, use a clear placeholder like `"/path/obtained/from/reference"` or infer a reasonable path structure.
*   Wildcards: Use wildcards outside quotes for file matching (globbing), e.g., `rm *.tmp`, `mv "target dir/"?.txt ./`. Avoid constructs like `rm "*.tmp"`.


Proceed with the first task.
"""),
            ],
        ),
        # types.Content(
        #     role="model",
        #     parts=[
        #         types.Part.from_text(text="""echo okay"""),
        #     ],
        # ),
        # types.Content(
        #     role="user",
        #     parts=[
        #         types.Part.from_text(text="""open CSE Bros"""),
        #     ],
        # ),
        # types.Content(
        #     role="model",
        #     parts=[
        #         types.Part.from_text(text="""start '' '/c/Users/santh/Downloads/CSE_BROS.csv'"""),
        #     ],
        # ),
        # types.Content(
        #     role="user",
        #     parts=[
        #         types.Part.from_text(text="""Create a javascript file and a python file in videos and show them in the file explorer"""),
        #     ],
        # ),
        # types.Content(
        #     role="model",
        #     parts=[
        #         types.Part.from_text(text="""cd '/c/Users/santh/Videos/' && echo \"\" > script.js && echo \"\" > script.py && start ."""),
        #     ],
        # ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{prompt}"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""Return only command"""),
        ],
    )

    return client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
    ).text
        

if __name__ == "__main__":
    generate("find the largest file in the downloads folder and open it")