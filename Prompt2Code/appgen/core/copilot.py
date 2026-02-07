
import subprocess
from appgen.utils.console import console

class CopilotError(Exception):
    pass

def call_copilot(prompt: str, spinner_text="Consulting GitHub Copilot...") -> str:
    with console.status(f"[cyan]{spinner_text}[/cyan]", spinner="dots"):
        result = subprocess.run(
            ["gh", "copilot", "-p", prompt, "--silent"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            shell=False
        )

    if result.returncode != 0:
        raise CopilotError(result.stderr.strip())

    output = result.stdout.strip()
    if not output:
        raise CopilotError("Copilot returned empty output")

    return output

def get_copilot_suggestion(query, language, color_scheme="default", complex_app=False, architecture="Standard", extras=None):
    extras = extras or []
    
    lang_instruction = ""
    if language.lower() == "python":
        lang_instruction = (
            "Write a complete Python Streamlit application. "
            "List all required pip packages in a comment at the top: '# requirements: pkg1, pkg2'. "
            "Include error handling. "
            "IMPORTANT: Include a sidebar with an 'Intuitive User Interface (UI) Builder' section "
            "using Streamlit widgets."
        )
    elif language.lower() == "html":
        lang_instruction = (
            "Write a complete HTML app with CSS (Flexbox/Grid) and JS. "
            "Include a 'drag-and-drop' style editor interface simulation."
        )
    elif language.lower() == "c++":
        lang_instruction = "Write a complete C++ console app, compatible with WebAssembly if possible."
    else:
        lang_instruction = f"Write a complete application in {language}."

    complexity_instruction = ""
    if complex_app:
        complexity_instruction = (
            "This is a complex app. Separate files clearly.\n"
            "For each file, start with a line '### filename: <name>'.\n"
            "Then provide the code in a markdown block.\n"
            "Example:\n"
            "### filename: main.py\n"
            "```python\n...\n```"
        )
    else:
        complexity_instruction = "The code must be self-contained in a single file."

    full_prompt = (
        f"Primary Request: {query}\n"
        f"Specs:\n- Lang: {language}\n- Style: {color_scheme}\n- Arch: {architecture}\n"
        f"- Extras: {', '.join(extras)}\n"
        f"- Instructions: {lang_instruction}\n"
        f"- Structure: {complexity_instruction}\n\n"
        "Generate the code exactly matching requests."
    )
    
    return call_copilot(full_prompt, f"Consulting Copilot ({language}, {architecture})...")
