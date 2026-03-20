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

- ✅ Types code **line by line** with configurable line break behaviour
- ✅ Handles **special characters** correctly (`{`, `}`, `<`, `>`, `#`, `*`, etc.) via explicit shift+key combos
- ✅ **Auto-close bracket fix** — detects and removes editor-inserted closing `}` after every `{`
- ✅ **Ctrl+C hotkey** to stop the script instantly at any time
- ✅ Configurable **indent stripping** for editors that auto-indent (e.g. Moodle TinyMCE)
- ✅ Configurable **tab handling** — preserve as-is or convert to spaces
- ✅ Configurable **startup delay** to let you click the target text box
- ✅ Configurable **typing speed**
- ✅ Built-in **fail-safe**: move the mouse to any screen corner to abort instantly
- ✅ Works on **Windows 10 / 11**
- ✅ Supports any plain-text source file (`.py`, `.c`, `.cpp`, `.js`, `.java`, etc.)

---

## Requirements

- Python **3.10+**
- [`pyautogui`](https://pyautogui.readthedocs.io/en/latest/)
- [`keyboard`](https://pypi.org/project/keyboard/)

---

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/probabalyabot/Autotyper-for-assignments.git
cd auto-typer
```

**2. Install dependencies:**

```bash
pip install pyautogui keyboard
```

---

## Usage

**1.** Place your source code file in the project folder (e.g., `code.py`, `code.c`, `code.cpp`).

**2.** Open `auto_typer.py` and set the `CODE_FILE` variable to your file's name:

```python
CODE_FILE = "code.c"   # ← change this every time for different files
```

**3.** Run as Administrator (required by the `keyboard` library on Windows):

```bash
# Right-click terminal → "Run as administrator", then:
python auto_typer.py
```

**4.** You'll see a **5-second countdown** in the terminal — use this time to click inside the target text box.

**5.** The script will begin typing automatically. Press **Ctrl+C** at any time to stop.

---

## Configuration

All settings are at the **top of `auto_typer.py`** for easy access:

| Variable | Default | Description |
|---|---|---|
| `CODE_FILE` | `"code.c"` | Path to the source file to type |
| `STARTUP_DELAY` | `5` | Seconds to wait before typing starts |
| `CHAR_INTERVAL` | `0.03` | Delay between each character (in seconds) |
| `LINE_DELAY` | `0.05` | Pause after each line break |
| `USE_SHIFT_ENTER` | `True` | Use Shift+Enter instead of Enter to suppress Moodle auto-indent |
| `CONVERT_TABS` | `False` | Convert tabs to spaces before typing |
| `TAB_SIZE` | `4` | Spaces per tab (only used if `CONVERT_TABS = True`) |
| `STRIP_INDENT` | `True` | Strip leading whitespace and let the editor handle indentation |
| `AUTO_CLOSE_BRACKETS` | `True` | Press Delete after `{` to remove editor auto-inserted `}` |

### Typing Speed Guide

| `CHAR_INTERVAL` | Speed |
|---|---|
| `0.01` | Very fast |
| `0.03` | Fast *(default)* |
| `0.05` | Natural human pace |
| `0.08` | Slow / deliberate |

### Quick Config Reference

| Target | Recommended Settings |
|---|---|
| Moodle (TinyMCE rich text) | `USE_SHIFT_ENTER=True`, `STRIP_INDENT=True`, `AUTO_CLOSE_BRACKETS=True` |
| Plain textarea | `USE_SHIFT_ENTER=False`, `STRIP_INDENT=False`, `AUTO_CLOSE_BRACKETS=False` |
| VS Code / code editor | `USE_SHIFT_ENTER=False`, `STRIP_INDENT=False`, `CONVERT_TABS=False` |

---

## How It Works

```
User runs script
      │
      ▼
 Reads source file
 (optional: strip indent, convert tabs)
      │
      ▼
  Countdown timer
 (user clicks textbox)
      │
      ▼
 For each line:
  ├─ Normal char? → keyboard.write()
  ├─ Special char ({, }, <, >, etc.)? → pyautogui.hotkey("shift", key)
  ├─ Typed a {? → press Delete to remove auto-inserted }
  └─ Press Shift+Enter (or Enter)
      │
      ▼
    Done ✅
```

Special characters like `{`, `}`, `(`, `)`, `<`, `>`, `#`, `*` are typed using explicit `shift+key` hotkey combos mapped to the US keyboard layout, bypassing the unreliable character translation in `keyboard.write()` and `pyautogui.write()`. All other characters are typed via `keyboard.write()`.

---

## Tips & Troubleshooting

**🛑 To stop the script immediately:**
- Press **Ctrl+C** anywhere — the script stops cleanly at the end of the current line
- Or move your mouse to **any corner of the screen** (PyAutoGUI fail-safe)

**⚠️ Getting extra `}` brackets?**
- Enable `AUTO_CLOSE_BRACKETS = True` — the editor is auto-closing `{` and the script will delete the extra `}`

**⚠️ Indentation is cascading / compounding?**
- Enable `STRIP_INDENT = True` — lets the editor handle indentation entirely
- Enable `USE_SHIFT_ENTER = True` — suppresses Moodle's paragraph-level auto-indent

**⚠️ Characters being mistyped or skipped?**
- Ensure the file is saved as **UTF-8**
- Slightly increase `CHAR_INTERVAL` (e.g. `0.05`)

**⚠️ Script types in the wrong window?**
- Increase `STARTUP_DELAY` to give yourself more time to click the correct field

**⚠️ Permission error on startup?**
- Run the terminal as Administrator — the `keyboard` library requires elevated permissions on Windows

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with annoyance at Moodle using Python & PyAutoGUI</p>