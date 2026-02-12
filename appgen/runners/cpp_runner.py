
import subprocess
import sys
import shutil
import webbrowser
from rich.prompt import Confirm
from appgen.utils.console import console

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_online_cpp_programiz(code_content):
    """
    Automates running C++ code on Programiz online compiler.
    """
    PROGRAMIZ_URL = "https://www.programiz.com/cpp-programming/online-compiler/"
    
    if not Confirm.ask("Open browser automation for Programiz? (Select No to just open website)"):
        webbrowser.open(PROGRAMIZ_URL)
        return

    console.print("[cyan]Launching Selenium automation for Programiz C++ Compiler...[/cyan]")
    console.print("[dim]This requires Chrome browser installed.[/dim]")
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        # Keep browser open after script finishes
        options.add_experimental_option("detach", True) 
        
        # Suppress logging
        options.add_argument("--log-level=3")
        
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
        console.print(f"[green]Opening {PROGRAMIZ_URL}...[/green]")
        driver.get(PROGRAMIZ_URL)

        # Wait for editor
        wait = WebDriverWait(driver, 15)
        # Programiz uses Ace editor, typically in a #editor div
        wait.until(EC.presence_of_element_located((By.ID, "editor")))
        
        console.print("[cyan]Injecting code into editor...[/cyan]")
        # Escape backticks and backslashes for JS string
        safe_code = code_content.replace("\\", "\\\\").replace("`", "\\`")
        
        # Use Ace API to set value
        driver.execute_script(f'ace.edit("editor").setValue(`{safe_code}`);')
        
        console.print("[cyan]Clicking Run button...[/cyan]")
        # Find Run button - it usually has text "Run"
        run_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Run')]")))
        run_button.click()
        
        console.print("[bold green]Code submitted! Check the browser window for output.[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]Automation Error:[/bold red] {e}")
        console.print("[yellow]Falling back to opening the website only...[/yellow]")
        webbrowser.open(PROGRAMIZ_URL)

def run_cpp_app(file_path):
    if shutil.which("g++"):
        # Compiler exists, try to run
        exe_path = file_path.replace(".cpp", ".exe" if sys.platform == "win32" else "")
        app_dir = os.path.dirname(os.path.abspath(file_path))
        
        console.print("[cyan]Compiling locally...[/cyan]")
        # Compiling in the same directory
        compile_result = subprocess.run(["g++", file_path, "-o", exe_path], capture_output=True, text=True)
        
        if compile_result.returncode == 0:
            console.print("[cyan]Running in new console...[/cyan]")
            if sys.platform == "win32":
                os.system(f'start cmd /k "{exe_path}"')
            else:
                subprocess.run([exe_path], cwd=app_dir)
            return

    # If no compiler or compilation failed, use Online Automation
    console.print("[yellow]Local C++ compiler not found. Using Programiz Online Compiler...[/yellow]")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
        run_online_cpp_programiz(code_content)
    except Exception as e:
        console.print(f"[red]Error reading C++ file: {e}[/red]")
