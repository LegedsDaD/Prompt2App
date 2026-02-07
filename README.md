# Prompt2App
An advanced terminal-based application generator and manager powered by GitHub Copilot CLI.
This tool lets you generate, refine, analyze, run, and manage applications using AI — all from a rich interactive CLI interface.

Think of it as a mini AI-powered IDE + app factory inside your terminal.

## ✨ Key Features

### 🚀 App Generation

Generate complete applications using GitHub Copilot

Supports:

Python (Streamlit, CLI apps)

HTML/CSS/JavaScript

C++

Choose:

>>Simple or Complex (multi-file) apps

>>Architecture style (Standard, MVC, Microservices)

>>Color/UI themes

>>Extra features (README, Docker hints, tests)

### 🤖 Multi-Agent Copilot Simulation

Simulates a team of AI agents:

>>Architect Agent – designs system structure

>>Developer Agent – writes code

>>Reviewer Agent – validates output

This mode is slower but produces higher-quality designs.

### 💬 Chat With Copilot (Live Code Assistance)

Chat interactively with Copilot about a generated app

Copilot can:

>>Explain logic

>>Suggest improvements

>>Rewrite files

>>Optional automatic application of suggested code (with backup)

### 🧪 Health Check & Code Analysis

Static analysis for Python apps:

>>Syntax errors

>>Empty functions

>>Dangerous calls (eval, exec, etc.)

Code quality scoring:

>>Readability

>>Security

>>Performance

### 🏗 Architecture Explanation

Ask why a particular architecture was chosen

Understand design trade-offs and benefits

### ▶ Run & Preview Apps

Run Python, HTML, and C++ apps directly

>Auto-detects:

>>Streamlit apps

>>Main files

>>HTML apps open in browser

>>C++ apps compile locally or run online (Programiz fallback)

## 📦 App Management System

All generated apps are stored in a local registry

Features include:

>>View existing apps

>>Preview source code safely

>>Refine or regenerate apps

>>Export apps as ZIP

>>Create backups before changes


## 🧰 Tech Stack

>>Python 3.9+

>>GitHub CLI + Copilot Extension

>>Rich – terminal UI

>>Questionary – interactive menus

>>Selenium – optional online C++ execution

>>AST – static code analysis

## 📋 Requirements
System Requirements

>>Python 3.9 or higher

>>GitHub account with Copilot access

>>GitHub CLI installed

>>Python Dependencies

>>Install dependencies using:
```bash
pip install rich questionary selenium webdriver-manager
```
```
gh auth login
```
```
gh extension install github/gh-copilot
```
▶ How to Run
```
python main.py
```

You’ll see an interactive menu with options to:

>>Create a new app

>>View or run existing apps

>>Refine or fix apps

>>Exit

## 📁 Project Structure
```
appgen/
│
├── core/
│   ├── copilot.py
│   ├── registry.py
│   ├── extractor.py
│   ├── scorer.py
│
├── runners/
│   ├── python_runner.py
│   ├── cpp_runner.py
│   ├── html_runner.py
│
├── ui/
│   ├── splash.py
│   ├── menus.py
│
├── utils/
│   ├── backup.py
│   ├── health.py
│   ├── filesystem.py
│
├── main.py
└── apps_registry.json
```
