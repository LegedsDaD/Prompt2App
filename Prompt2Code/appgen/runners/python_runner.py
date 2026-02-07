
import subprocess
import sys
import re
from appgen.utils.console import console

def run_python_app(file_path):
    # Try to install dependencies first
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Look for requirements comment
    req_match = re.search(r"#\s*requirements:\s*(.*)", content, re.IGNORECASE)
    if req_match:
        reqs = [r.strip() for r in req_match.group(1).split(",") if r.strip()]
        if reqs:
            console.print(f"[cyan]Installing dependencies: {', '.join(reqs)}[/cyan]")
            subprocess.run([sys.executable, "-m", "pip", "install"] + reqs, check=False)
    
    # Fallback: Naive import detection
    imports = re.findall(r"^import (\w+)|^from (\w+)", content, re.MULTILINE)
    detected_pkgs = set()
    for imp in imports:
        pkg = imp[0] or imp[1]
        if pkg and pkg not in sys.builtin_module_names and pkg not in ['streamlit']:
                detected_pkgs.add(pkg)
    
    # Heuristic: if it imports streamlit, run with streamlit
    if "import streamlit" in content:
        subprocess.run(["streamlit", "run", file_path], check=True)
    else:
        subprocess.run(["python", file_path], check=True)
