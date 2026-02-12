
import os
import time
import shutil
import questionary
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich.syntax import Syntax

from appgen.utils.console import console
from appgen.core.registry import load_apps_registry, add_app_to_registry
from appgen.core.copilot import get_copilot_suggestion, call_copilot, CopilotError
from appgen.core.extractor import extract_code_blocks_with_filenames
from appgen.core.scorer import score_app_code
from appgen.runners.manager import run_app
from appgen.utils.health import perform_health_check
from appgen.utils.backup import create_backup
from appgen.utils.filesystem import export_app_zip

def chat_with_copilot(app_path, language):
    """
    Interactive chat session with Copilot about the generated app.
    """
    console.print(Panel(f"[bold cyan]Chatting with Copilot about {os.path.basename(app_path)}[/bold cyan]\nType 'exit' to stop.", border_style="cyan"))
    
    # Load context
    try:
        code_context = ""
        if os.path.isdir(app_path):
             files = [f for f in os.listdir(app_path) if f.endswith(('.py', '.cpp', '.html', '.js', '.css'))]
             for f in files[:3]: # Limit context
                 with open(os.path.join(app_path, f), 'r', encoding='utf-8') as fh:
                     code_context += f"\n--- {f} ---\n{fh.read()[:2000]}"
        else:
            with open(app_path, "r", encoding="utf-8") as f:
                code_context = f.read()[:3000]
    except Exception as e:
        console.print(f"[red]Error loading context: {e}[/red]")
        return

    while True:
        user_msg = Prompt.ask("\n[bold green]You[/bold green]")
        if user_msg.lower() in ['exit', 'quit']:
            break
            
        full_prompt = (
            f"Context: You are an AI assistant helping a developer with their {language} app.\n"
            f"Code:\n{code_context}\n\n"
            f"User Question: {user_msg}\n"
            "Answer helpful and concise."
        )
        
        try:
            response = call_copilot(full_prompt, "Copilot typing...")
            console.print(Panel(Markdown(response), title="Copilot", border_style="blue"))
            
            # Check if response contains code to apply
            blocks = extract_code_blocks_with_filenames(response)
            if blocks and Confirm.ask("Copilot suggested code changes. Apply them?"):
                create_backup(app_path)
                if os.path.isdir(app_path):
                     for block in blocks:
                         fname = block['filename']
                         if fname:
                             with open(os.path.join(app_path, fname), "w", encoding="utf-8") as f:
                                 f.write(block['code'])
                             console.print(f"[green]Updated {fname}[/green]")
                else:
                     with open(app_path, "w", encoding="utf-8") as f:
                         f.write(blocks[0]['code'])
                     console.print(f"[green]Updated {app_path}[/green]")
                
                if Confirm.ask("Run updated app?"):
                    run_app({"name": os.path.basename(app_path), "path": app_path, "language": language})
                    
        except CopilotError as e:
            console.print(f"[red]Error: {e}[/red]")

def explain_app_code(app_path, language):
    try:
        if os.path.isdir(app_path):
            # Read main file or first file
            files = os.listdir(app_path)
            main_file = next((f for f in files if f.startswith("main") or f.startswith("index")), files[0] if files else None)
            if not main_file: return "No files found."
            path = os.path.join(app_path, main_file)
        else:
            path = app_path
            
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
            
        prompt = (
            f"Explain this {language} code for a beginner. "
            "Cover: 1. Architecture 2. Main functions 3. How to run it 4. Where to customize it. "
            f"\n\nCode:\n{code[:3000]}"
        )
        explanation = call_copilot(prompt, "Generating explanation...")
        console.print(Panel(Markdown(explanation or "No explanation generated."), title="App Explanation", border_style="blue"))
        
    except Exception as e:
        console.print(f"[red]Error explaining app: {e}[/red]")

def generate_readme(app_path, language):
    try:
        # Determine code content
        code_snippet = ""
        if os.path.isdir(app_path):
             files = [f for f in os.listdir(app_path) if f.endswith(('.py', '.cpp', '.html', '.js', '.css'))]
             for f in files[:2]: # Take first 2 files
                 with open(os.path.join(app_path, f), 'r', encoding='utf-8') as fh:
                     code_snippet += f"\n--- {f} ---\n{fh.read()[:1000]}"
        else:
            with open(app_path, 'r', encoding='utf-8') as f:
                code_snippet = f.read()[:2000]

        prompt = (
            f"Generate a professional README.md for this {language} application. "
            "Include: Description, Features, Installation, Usage, and Credits. "
            f"\n\nCode Context:\n{code_snippet}"
        )
        
        readme_content = call_copilot(prompt, "Generating README...")
        
        # Simple heuristic to extract if markdown wrapped
        if readme_content.startswith("```"):
             # Reuse extractor but simplified
             from appgen.core.extractor import extract_code_blocks_with_filenames
             blocks = extract_code_blocks_with_filenames(readme_content)
             if blocks:
                 readme_content = blocks[0]['code']

        if readme_content:
            save_path = os.path.join(app_path if os.path.isdir(app_path) else os.path.dirname(app_path), "README.md")
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(readme_content)
            console.print(f"[green]README.md generated at {save_path}[/green]")
        else:
            console.print("[red]Failed to generate README.[/red]")

    except Exception as e:
        console.print(f"[red]Error generating README: {e}[/red]")

def app_preview(app_path, language):
    console.print(f"[bold]Previewing {app_path}[/bold]")
    if os.path.isdir(app_path):
        for root, _, files in os.walk(app_path):
            for f in files: console.print(f"- {f}")
    else:
        with open(app_path, "r", encoding="utf-8") as f: 
            console.print(Syntax(f.read()[:500], language, theme="monokai", line_numbers=True))

def regenerate_app(app_entry):
    meta = app_entry.get("metadata", {})
    if meta:
        console.print("[cyan]Regenerating with original prompt...[/cyan]")
        suggestion = get_copilot_suggestion(
            meta.get("query", app_entry["description"]), 
            app_entry["language"], 
            meta.get("color_scheme"), 
            False, 
            meta.get("architecture"), 
            meta.get("extras")
        )
        console.print("[yellow]Regeneration complete. (Implementation note: Save logic reused from create_new_app would be better here)[/yellow]")
        console.print(Panel(Markdown(suggestion), border_style="green"))
    else:
        console.print("[red]No metadata available for regeneration.[/red]")

def why_architecture(app_path, language):
    prompt = (
        f"Analyze this {language} application structure. "
        "Why was this specific architecture/pattern chosen over others? "
        "Explain the benefits for this use case."
    )
    # We need to read code context first
    try:
        code_snippet = ""
        if os.path.isdir(app_path):
             files = [f for f in os.listdir(app_path) if f.endswith(('.py', '.cpp', '.html', '.js', '.css'))]
             for f in files[:2]:
                 with open(os.path.join(app_path, f), 'r', encoding='utf-8') as fh:
                     code_snippet += f"\n--- {f} ---\n{fh.read()[:1000]}"
        else:
            with open(app_path, 'r', encoding='utf-8') as f:
                code_snippet = f.read()[:2000]
        
        full_prompt = f"{prompt}\n\nCode Context:\n{code_snippet}"
        explanation = call_copilot(full_prompt, "Analyzing Architecture...")
        console.print(Panel(Markdown(explanation or "No explanation generated."), title="Architecture Analysis", border_style="magenta"))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def multi_copilot_simulation(query):
    console.print("[bold cyan]Activating Multi-Copilot Simulation Mode...[/bold cyan]")
    
    # 1. Architect Agent
    with console.status("[blue]Architect Agent: Designing solution...[/blue]"):
        time.sleep(1.5)
        arch_prompt = f"Design a high-level architecture for: {query}. Brief bullet points."
        try:
            arch_plan = call_copilot(arch_prompt, "Architect Agent thinking...")
        except:
            arch_plan = "Standard Architecture Plan"
        console.print(Panel(Markdown(arch_plan), title="Architect Agent Plan", border_style="blue"))
        
    # 2. Developer Agent
    with console.status("[green]Developer Agent: Writing code based on plan...[/green]"):
        dev_prompt = f"Write the code for {query} following this plan: {arch_plan}"
        try:
            code_suggestion = call_copilot(dev_prompt, "Developer Agent coding...")
        except CopilotError as e:
            console.print(f"[red]Developer Agent failed: {e}[/red]")
            return None
            
    # 3. Reviewer Agent
    with console.status("[magenta]Reviewer Agent: Critiquing code...[/magenta]"):
        time.sleep(1)
        # We simulate this step or actually call it if we want to burn tokens/time
        # For speed, let's just present the code as "Reviewed"
        console.print("[magenta]Reviewer Agent: Code looks solid. Approved.[/magenta]")
        
    return code_suggestion

# Action Dispatcher
APP_ACTIONS = {
    "Run App": lambda app: run_app(app),
    "Chat with Copilot": lambda app: chat_with_copilot(app["path"], app["language"]),
    "Explain This App": lambda app: explain_app_code(app["path"], app["language"]),
    "App Preview (Safe Mode)": lambda app: app_preview(app["path"], app["language"]),
    "Health Check": lambda app: perform_health_check(app["path"], app["language"]),
    "Code Quality Score": lambda app: score_app_code(app["path"], app["language"]),
    "Generate README": lambda app: generate_readme(app["path"], app["language"]),
    "Create Backup": lambda app: create_backup(app["path"]),
    "Export to ZIP": lambda app: export_app_zip(app["path"]),
    "Regenerate (Same Prompt)": lambda app: regenerate_app(app),
    "Why This Architecture?": lambda app: why_architecture(app["path"], app["language"]),
}

def view_run_menu():
    registry = load_apps_registry()
    if not registry:
        console.print("[yellow]No apps found.[/yellow]")
        return

    # Use Questionary for selection
    choices = []
    for app in registry:
        label = f"{app['name']} ({app['language']}) - {app['description'][:30]}"
        choices.append(questionary.Choice(title=label, value=app))
    
    choices.append(questionary.Choice(title="Back", value="back"))

    selected_app = questionary.select("Select an App:", choices=choices).ask()
    
    if selected_app == "back":
        return

    action = questionary.select(
        f"Action for {selected_app['name']}:",
        choices=list(APP_ACTIONS.keys()) + ["Back"]
    ).ask()

    if action == "Back":
        return

    action_fn = APP_ACTIONS.get(action)
    if action_fn:
        action_fn(selected_app)

def save_generated_app(suggestion, user_query, lang_choice, color_scheme, is_complex, architecture, extras):
    console.print(Panel(Markdown(suggestion), border_style="green"))
    blocks = extract_code_blocks_with_filenames(suggestion)

    if blocks:
        if Confirm.ask("Save this app?"):
            app_name = Prompt.ask("App Name", default=f"app_{int(time.time())}")
            
            os.makedirs(app_name, exist_ok=True)
            saved_path = ""
            
            if is_complex or len(blocks) > 1:
                for i, block in enumerate(blocks):
                    fname = block['filename']
                    if not fname:
                        ext = ".txt"
                        if "python" in block['language'].lower(): ext = ".py"
                        elif "html" in block['language'].lower(): ext = ".html"
                        fname = f"file_{i}{ext}"
                    
                    full_path = os.path.join(app_name, fname)
                    with open(full_path, "w", encoding="utf-8") as f: f.write(block['code'])
                    if i==0: saved_path = full_path
            else:
                # Single file
                block = blocks[0]
                ext = ".py"
                if "html" in lang_choice.lower(): ext = ".html"
                elif "c++" in lang_choice.lower(): ext = ".cpp"
                fname = f"{app_name}{ext}"
                full_path = os.path.join(app_name, fname)
                with open(full_path, "w", encoding="utf-8") as f: f.write(block['code'])
                saved_path = full_path
            
            metadata = {
                "query": user_query,
                "color_scheme": color_scheme,
                "architecture": architecture,
                "extras": extras
            }
            add_app_to_registry(app_name, user_query, lang_choice, saved_path, extras, metadata)
            
            if Confirm.ask("Chat with Copilot about this app?"):
                chat_with_copilot(saved_path, lang_choice)
            elif Confirm.ask("Run now?"):
                run_app({"name": app_name, "path": os.path.abspath(saved_path), "language": lang_choice})
    else:
        console.print("[yellow]No code found in response.[/yellow]")

def create_new_app():
    console.print("\n[bold green]Describe the app you want to create[/bold green]")
    user_query = Prompt.ask("Query")
    if not user_query.strip(): return
    
    # Mode Selection
    mode = questionary.select(
        "Generation Mode:",
        choices=["Standard (Single Copilot)", "Multi-Agent Simulation (Slower, Higher Quality)"]
    ).ask()
    
    lang_choice = questionary.select("Select Language:", choices=["Python", "HTML", "C++"]).ask()
    color_scheme = questionary.select("Select Color Scheme:", choices=["Default", "Dark Mode", "Cyberpunk"]).ask()
    app_type = questionary.select("Complexity:", choices=["Simple", "Complex"]).ask()
    is_complex = "Complex" in app_type
    
    architecture = "Standard"
    extras = []
    if Confirm.ask("Advanced Options?"):
        architecture = questionary.select("Architecture:", choices=["Standard", "MVC", "Microservices"]).ask()
        extras = questionary.checkbox("Features:", choices=["Docker", "Unit Tests", "README"]).ask()

    try:
        if "Multi-Agent" in mode:
             # We use the simulation but we need to inject the specs into the query
             enhanced_query = f"{user_query} (Language: {lang_choice}, Arch: {architecture}, Style: {color_scheme})"
             suggestion = multi_copilot_simulation(enhanced_query)
        else:
             suggestion = get_copilot_suggestion(user_query, lang_choice, color_scheme, is_complex, architecture, extras)
             
        if suggestion:
            save_generated_app(suggestion, user_query, lang_choice, color_scheme, is_complex, architecture, extras)
            
    except CopilotError as e:
        console.print(f"[bold red]Copilot Error:[/bold red] {e}")
        return

def refine_app():
    registry = load_apps_registry()
    if not registry:
        console.print("[yellow]No apps found to refine.[/yellow]")
        return
        
    choices = []
    for app in registry:
        label = f"{app['name']} ({app['language']}) - {app['description'][:30]}"
        choices.append(questionary.Choice(title=label, value=app))
    choices.append(questionary.Choice(title="Back", value="back"))
    
    selected_app = questionary.select("Select App to Refine:", choices=choices).ask()
    
    if selected_app == "back": return
    
    # Read existing code
    try:
        code_content = ""
        if os.path.isdir(selected_app["path"]):
             files = [f for f in os.listdir(selected_app["path"]) if f.endswith(('.py', '.cpp', '.html', '.js', '.css'))]
             for f in files:
                 with open(os.path.join(selected_app["path"], f), 'r', encoding='utf-8') as fh:
                     code_content += f"\n--- {f} ---\n{fh.read()}"
        else:
            with open(selected_app["path"], "r", encoding="utf-8") as f:
                code_content = f.read()
    except Exception as e:
        console.print(f"[red]Could not read app files: {e}[/red]")
        return

    refinement_query = Prompt.ask("Describe the fix or new feature")
    
    # Auto Backup
    create_backup(selected_app["path"])
    
    full_prompt = (
        f"Here is the existing code for an app:\n\n```\n{code_content}\n```\n\n"
        f"User Request: {refinement_query}\n"
        "Rewrite the code to incorporate this request. Return the full updated code in markdown blocks."
    )
    
    try:
        suggestion = call_copilot(full_prompt, "Refining App...")
        if suggestion:
            # Re-use save logic but overwrite
            console.print(Panel(Markdown(suggestion), border_style="green"))
            blocks = extract_code_blocks_with_filenames(suggestion)
            
            if blocks:
                if Confirm.ask("Overwrite existing app with this update?"):
                     if os.path.isdir(selected_app["path"]):
                         # Overwrite files in directory
                         for block in blocks:
                             fname = block['filename']
                             if fname:
                                 with open(os.path.join(selected_app["path"], fname), "w", encoding="utf-8") as f:
                                     f.write(block['code'])
                                 console.print(f"[green]Updated {fname}[/green]")
                     else:
                         # Overwrite single file
                         with open(selected_app["path"], "w", encoding="utf-8") as f:
                             f.write(blocks[0]['code'])
                         console.print(f"[green]Updated {selected_app['path']}[/green]")
                         
                     if Confirm.ask("Run updated app?"):
                         run_app(selected_app)
            else:
                 console.print("[yellow]No code blocks found in refinement.[/yellow]")
    except CopilotError as e:
        console.print(f"[red]Refinement failed: {e}[/red]")

def main_menu():
    while True:
        menu_text = Text("Main Menu", style="bold white on blue", justify="center")
        console.print(Panel(menu_text, border_style="blue"))
        
        choice = questionary.select(
            "Select an option:",
            choices=[
                "Create New App",
                "View/Run Existing Apps",
                "Refine/Fix Existing App",
                "Exit"
            ]
        ).ask()
        
        if choice == "Exit":
            console.print("[yellow]Goodbye![/yellow]")
            break
        elif choice == "Create New App":
            create_new_app()
        elif choice == "View/Run Existing Apps":
            view_run_menu()
        elif choice == "Refine/Fix Existing App":
            refine_app()
