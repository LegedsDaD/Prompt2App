
import ast
import os
from rich.panel import Panel
from rich.prompt import Confirm
from appgen.utils.console import console

DANGEROUS_CALLS = {"eval", "exec", "os.system", "subprocess.Popen", "subprocess.call", "subprocess.run"}

def detect_dangerous_calls(tree):
    findings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = ""
            if isinstance(node.func, ast.Name):
                name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                name = node.func.attr # This might catch 'system' in 'os.system'
                # Better check for full path if possible, but simple name check is a start
            
            # Simple check for direct usage or attribute usage
            # This is heuristic.
            if name in DANGEROUS_CALLS:
                findings.append(f"Dangerous call detected: {name}")
    return findings

def perform_health_check(app_path, language):
    console.print("[bold]Running Health Check...[/bold]")
    issues = []
    
    try:
        if language.lower() == "python":
            files = []
            if os.path.isdir(app_path):
                files = [os.path.join(app_path, f) for f in os.listdir(app_path) if f.endswith(".py")]
            elif app_path.endswith(".py"):
                files = [app_path]
                
            for file_p in files:
                with open(file_p, "r", encoding="utf-8") as f:
                    code = f.read()
                try:
                    tree = ast.parse(code)
                    
                    # Check imports
                    imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
                    from_imports = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) if node.module]
                    all_imports = imports + from_imports
                    
                    if not all_imports:
                        issues.append(f"{os.path.basename(file_p)}: No imports found (might be okay for simple scripts).")
                    
                    # Check dangerous calls
                    dang = detect_dangerous_calls(tree)
                    for d in dang:
                        issues.append(f"{os.path.basename(file_p)}: {d}")

                    # Check for empty functions
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                                issues.append(f"{os.path.basename(file_p)}: Function '{node.name}' is empty (pass).")
                                
                except SyntaxError as e:
                    issues.append(f"{os.path.basename(file_p)}: Syntax Error - {e}")
                    
    except Exception as e:
        issues.append(f"Analysis failed: {e}")
        
    if issues:
        console.print(Panel("\n".join(issues), title="Health Check Issues", border_style="red"))
    else:
        console.print(Panel("No obvious issues found. Code looks healthy!", title="Health Check Passed", border_style="green"))

def confirm_dangerous_execution():
    console.print(
        Panel(
            "⚠ This app was AI-generated and may execute system commands.\n"
            "Run only if you trust the code.",
            border_style="red"
        )
    )
    return Confirm.ask("Proceed anyway?")
