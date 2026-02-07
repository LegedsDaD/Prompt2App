
import os
import sys
from appgen.utils.console import console
from appgen.utils.health import confirm_dangerous_execution
from appgen.runners.python_runner import run_python_app
from appgen.runners.html_runner import run_html_app
from appgen.runners.cpp_runner import run_cpp_app

def run_app(app_entry):
    """
    Runs the app based on its language.
    """
    if not confirm_dangerous_execution():
        return

    file_path = app_entry["path"]
    language = app_entry.get("language", "auto").lower()
    
    console.print(f"[bold green]Running {app_entry['name']}...[/bold green]")
    
    try:
        if language == "python" or file_path.endswith(".py"):
            run_python_app(file_path)
        elif language == "html" or file_path.endswith(".html"):
            run_html_app(file_path)
        elif language == "c++" or file_path.endswith(".cpp"):
            run_cpp_app(file_path)
        else:
            console.print(f"[yellow]Unknown runner for language {language}. Opening file...[/yellow]")
            if sys.platform == "win32":
                 os.startfile(file_path)
    except KeyboardInterrupt:
        console.print("\n[yellow]App stopped.[/yellow]")
    except Exception as e:
        console.print(f"[bold red]Error running app:[/bold red] {e}")
