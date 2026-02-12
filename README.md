# Prompt2App 🚀

> **Turn your ideas into running applications in seconds using the power of GitHub Copilot.**

Prompt2App is an advanced, terminal-based application generator and manager. It leverages the GitHub Copilot CLI to generate, refine, analyze, run, and manage applications through a rich, interactive command-line interface.

Think of it as a **mini AI-powered IDE + App Factory** right in your terminal.

---

## ✨ Key Features

### 🚀 **AI App Generation**
Generate complete, functional applications by simply describing them.
- **Languages:** Python (Streamlit, CLI), HTML/CSS/JS, C++.
- **Modes:** 
    - **Standard:** Quick generation using a single Copilot instance.
    - **Multi-Agent Simulation:** Simulates a team (Architect, Developer, Reviewer) for higher quality, architecturally sound apps.
- **Customization:** Choose themes (Cyberpunk, Dark Mode, etc.), architectures (MVC, Microservices), and complexity levels.

### 📁 **Organized Workspace**
- **Automatic Project Structure:** Every generated app is saved in its own dedicated subdirectory.
- **Registry System:** Tracks all your generated apps, keeping your workspace clean and organized.

### 🤖 **Interactive Copilot Chat**
Talk to your codebase!
- **Context-Aware:** Chat with Copilot about *specific* apps you've generated.
- **Live Refinement:** Ask Copilot to fix bugs, add features, or explain code, and apply changes directly.

### 🏃 **Instant Execution**
Run your apps immediately after generation.
- **Python:** Auto-detects dependencies and runs Streamlit or standard CLI apps.
- **HTML:** Opens instantly in your default browser.
- **C++:** Compiles locally using `g++` or falls back to browser-based automation (Programiz) if no compiler is found.

### 🛡️ **Health & Quality Analysis**
- **Static Analysis:** Checks for syntax errors and dangerous code patterns.
- **Quality Scoring:** Rates your app on readability, security, and performance.
- **Architecture Insights:** Ask *why* a certain architecture was chosen.

---

## 🛠️ Installation

### Prerequisites
1. **Python 3.9+**
2. **GitHub CLI (`gh`)** installed and authenticated.
3. **GitHub Copilot Extension** for CLI.

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Prompt2App.git
   ```
   ```bash
   cd Prompt2App
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If `requirements.txt` is missing, install the core packages:*
   ```bash
   pip install rich questionary selenium webdriver-manager
   ```

3. **Check GitHub Auth:**
   Ensure you are logged in and have the Copilot extension:
   ```bash
   gh auth login
   ```
   ```bash
   gh extension install github/gh-copilot
   ```
   ```bash
   gh copilot --version
   ```

---

## 🎮 Usage

Run the main application:
```bash
python main.py
```

### Main Menu Options

1.  **Create New App**
    - Enter your prompt (e.g., "A snake game with neon graphics").
    - Select mode: **Standard** or **Multi-Agent**.
    - Choose language, complexity, and style.
    - **Save & Run:** The app will be generated in a new folder (e.g., `snake_game/`).

2.  **View/Run Existing Apps**
    - Browse your registry of generated apps.
    - Perform actions: Run, Chat, Explain, Preview, Health Check, etc.

3.  **Refine/Fix Existing App**
    - Select an app and describe the change (e.g., "Make the snake move faster").
    - Copilot will regenerate the code, and you can overwrite the existing files safely (backups are created automatically).

---

## 📂 Project Structure

```
Prompt2App/
├── appgen/
│   ├── core/           # Core logic (Copilot interface, registry, analysis)
│   ├── runners/        # Language-specific runners (Python, HTML, C++)
│   ├── ui/             # UI components (Menus, Splash screen)
│   └── utils/          # Helpers (Filesystem, Console, Backup)
├── apps_registry.json  # Database of generated apps
├── main.py             # Entry point
└── README.md           # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License. See `LICENSE` for more details.
