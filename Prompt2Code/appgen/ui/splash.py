
import time
import random
import shutil
import sys
import os
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from appgen.utils.console import console
from appgen.core.registry import load_apps_registry

def show_splash_screen():
    console.clear()
    
    # Advanced System Boot Simulation
    console.print(Panel("[bold cyan]INITIALIZING ADVANCED APP GENERATOR CORE[/bold cyan]", border_style="cyan"))
    time.sleep(0.5)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task1 = progress.add_task("[green]Checking System Resources...", total=100)
        task2 = progress.add_task("[cyan]Connecting to Neural Network...", total=100)
        task3 = progress.add_task("[magenta]Loading Architecture Modules...", total=100)
        
        while not progress.finished:
            if not progress.finished:
                progress.update(task1, advance=random.randint(2, 5))
            if progress.tasks[0].completed > 30:
                progress.update(task2, advance=random.randint(1, 4))
            if progress.tasks[1].completed > 50:
                progress.update(task3, advance=random.randint(3, 6))
            time.sleep(0.05)
            
    # System Status Table
    table = Table(title="System Status", show_header=True, header_style="bold magenta")
    table.add_column("Module", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="yellow")
    
    # Get basic system info
    os_info = f"{sys.platform} ({os.name})"
    py_version = sys.version.split()[0]
    gh_status = "Connected" if shutil.which("gh") else "Not Found"
    
    table.add_row("Operating System", "ONLINE", os_info)
    table.add_row("Python Environment", "ONLINE", f"v{py_version}")
    table.add_row("GitHub Copilot CLI", "ACTIVE" if "Connected" in gh_status else "ERROR", gh_status)
    table.add_row("App Registry", "LOADED", f"{len(load_apps_registry())} apps")
    
    console.print(table)
    console.print("\n[bold green]>> SYSTEM READY. WAITING FOR INPUT...[/bold green]\n")
    time.sleep(1)
