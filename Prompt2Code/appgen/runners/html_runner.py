
import webbrowser
import os
from appgen.utils.console import console

def run_html_app(file_path):
    # Open in default browser
    url = "file://" + os.path.abspath(file_path)
    console.print(f"[green]Opening {url}...[/green]")
    webbrowser.open(url)
