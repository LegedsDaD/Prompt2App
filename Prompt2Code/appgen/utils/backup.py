
import os
import shutil
import time
from appgen.utils.console import console

def create_backup(app_path):
    try:
        if os.path.isdir(app_path):
            backup_name = f"{app_path}_backup_{int(time.time())}"
            shutil.copytree(app_path, backup_name)
            console.print(f"[green]Backup created: {backup_name}[/green]")
        else:
            backup_name = f"{app_path}.bak_{int(time.time())}"
            shutil.copy(app_path, backup_name)
            console.print(f"[green]Backup created: {backup_name}[/green]")
    except Exception as e:
        console.print(f"[red]Backup failed: {e}[/red]")
