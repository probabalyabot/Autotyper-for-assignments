# 🤖 Auto-Typer — PyAutoGUI Code Typing Script

> Simulates human typing of code into any text field — even when **copy-paste is disabled**.

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Tips & Troubleshooting](#tips--troubleshooting)
- [License](#license)

---

## About

**Auto-Typer** is a lightweight Python script that reads source code from a file and types it out — character by character — into any active text field on your screen. It's designed for situations where copy-paste is blocked (e.g., online coding exams, restricted editors, or browser-based IDEs).

---

## Features

- ✅ Types code **line by line**, pressing `Enter` after each line
- ✅ Preserves **exact indentation** from the source file
- ✅ Automatically converts **tabs → 4 spaces** to prevent indentation issues
- ✅ Handles **special characters** correctly (`{`, `}`, `<`, `>`, `#`, `[]`, etc.)
- ✅ Configurable **startup delay** to let you click the target text box
- ✅ Configurable **typing speed** (characters per second)
- ✅ Built-in **fail-safe**: move the mouse to any screen corner to abort instantly
- ✅ Works on **Windows 10 / 11**
- ✅ Supports any plain-text source file (`.py`, `.c`, `.cpp`, `.js`, `.java`, etc.)

---

## Requirements

- Python **3.10+**
- [`pyautogui`](https://pyautogui.readthedocs.io/en/latest/)

---

## Installation

**1. Clone the repository:**

```bash
git https://github.com/probabalyabot/Autotyper-for-assignments.git
cd auto-typer
```

**2. Install the dependency:**

```bash
pip install pyautogui
```

---

## Usage

**1.** Place your source code file in the project folder (e.g., `code.py`, `code.c`, `code.cpp`).

**2.** Open `auto_typer.py` and set the `CODE_FILE` variable to your file's name:

```python
CODE_FILE = "code.c"   # ← change this
```

**3.** Run the script:

```bash
python auto_typer.py
```

**4.** You'll see a **5-second countdown** in the terminal — use this time to click inside the target text box / editor.

**5.** The script will begin typing automatically. Don't touch the mouse or keyboard until it finishes!

---

## Configuration

All settings are at the **top of `auto_typer.py`** for easy access:

| Variable | Default | Description |
|---|---|---|
| `CODE_FILE` | `"code.py"` | Path to the source file to type |
| `STARTUP_DELAY` | `5` | Seconds to wait before typing starts |
| `CHAR_INTERVAL` | `0.03` | Delay between each character (in seconds) |
| `LINE_DELAY` | `0.05` | Pause after pressing `Enter` each line |

### Typing Speed Guide

| `CHAR_INTERVAL` | Speed |
|---|---|
| `0.01` | Very fast |
| `0.03` | Fast *(default)* |
| `0.05` | Natural human pace |
| `0.08` | Slow / deliberate |

---

## How It Works

```
User runs script
      │
      ▼
 Reads source file
 (tabs → 4 spaces)
      │
      ▼
  Countdown timer
 (user clicks textbox)
      │
      ▼
 For each line:
  ├─ Type characters one by one
  └─ Press Enter
      │
      ▼
    Done ✅
```

The script uses `pyautogui.write()` with a per-character `interval` to properly handle special characters across different keyboard layouts on Windows.

---

## Tips & Troubleshooting

**🛑 To stop the script immediately:**
- Move your mouse to **any corner of the screen** (PyAutoGUI fail-safe), or
- Press `Ctrl+C` in the terminal window

**⚠️ Characters being mistyped or skipped?**
- Increase `CHAR_INTERVAL` (e.g., `0.05` or higher)
- Ensure the file is saved as **UTF-8**

**⚠️ Auto-indent is causing double indentation?**
- Increase `LINE_DELAY` slightly (e.g., `0.1`) to give the editor time to settle after `Enter`
- Make sure the target editor's auto-indent is turned off if possible

**⚠️ Script types in the wrong window?**
- Increase `STARTUP_DELAY` to give yourself more time to click the correct text field

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ using Python & PyAutoGUI</p>
