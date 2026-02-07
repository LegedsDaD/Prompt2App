
import os
import zipfile
import time
from appgen.utils.console import console

def export_app_zip(app_path):
    try:
        zip_name = f"app_export_{int(time.time())}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.isdir(app_path):
                for root, dirs, files in os.walk(app_path):
                    for file in files:
                        zipf.write(os.path.join(root, file), 
                                   os.path.relpath(os.path.join(root, file), os.path.join(app_path, '..')))
            else:
                zipf.write(app_path, os.path.basename(app_path))
        console.print(f"[green]App exported to {zip_name}[/green]")
    except Exception as e:
        console.print(f"[red]Export failed: {e}[/red]")
