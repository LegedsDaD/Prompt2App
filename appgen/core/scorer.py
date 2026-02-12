
import os
from rich.panel import Panel
from rich.markdown import Markdown
from appgen.core.copilot import call_copilot
from appgen.utils.console import console

def score_app_code(app_path, language):
    try:
        # Determine code content
        code_snippet = ""
        if os.path.isdir(app_path):
             files = [f for f in os.listdir(app_path) if f.endswith(('.py', '.cpp', '.html', '.js', '.css'))]
             for f in files[:2]:
                 with open(os.path.join(app_path, f), 'r', encoding='utf-8') as fh:
                     code_snippet += f"\n--- {f} ---\n{fh.read()[:1000]}"
        else:
            with open(app_path, 'r', encoding='utf-8') as f:
                code_snippet = f.read()[:2000]

        prompt = (
            f"Review this {language} code. "
            "Provide a score from 1-10 for: 1. Readability 2. Security 3. Performance. "
            "Briefly explain each score."
            f"\n\nCode:\n{code_snippet}"
        )
        
        review = call_copilot(prompt, "Scoring Code Quality...")
        console.print(Panel(Markdown(review or "No review generated."), title="Code Quality Score", border_style="magenta"))

    except Exception as e:
        console.print(f"[red]Error scoring app: {e}[/red]")
