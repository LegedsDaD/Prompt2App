
from appgen.ui.splash import show_splash_screen
from appgen.ui.menus import main_menu
import shutil
import sys
from appgen.utils.console import console

def check_dependencies():
    """Check if gh and gh copilot are installed."""
    if not shutil.which("gh"):
        console.print("[bold red]Error:[/bold red] GitHub CLI (gh) is not installed.")
        console.print("Please install it from https://cli.github.com/")
        sys.exit(1)

def main():
    show_splash_screen()
    check_dependencies()
    main_menu()

if __name__ == "__main__":
    main()
