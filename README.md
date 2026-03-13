# 🤖 Auto-Typer — PyAutoGUI Code Typing Script

> Simulates human typing of code into any text field — even when **copy-paste is disabled**.

---

##  Table of Contents

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

-  Types code **line by line**, pressing `Enter` after each line
-  Preserves **exact indentation** from the source file
-  Automatically converts **tabs → 4 spaces** to prevent indentation issues
-  Handles **special characters** correctly (`{`, `}`, `<`, `>`, `#`, `[]`, etc.) via clipboard injection
-  Configurable **startup delay** to let you click the target text box
-  Configurable **typing speed** (characters per second)
-  Built-in **fail-safe**: move the mouse to any screen corner to abort instantly
-  Works on **Windows 10 / 11**
-  Supports any plain-text source file (`.py`, `.c`, `.cpp`, `.js`, `.java`, etc.)

---

## Requirements

- Python **3.10+**
- [`pyautogui`](https://pyautogui.readthedocs.io/en/latest/)
- [`pyperclip`](https://pypi.org/project/pyperclip/)

---

## Installation

**1. Clone the repository:**

```bash
git clone https://github.com/probabalyabot/Autotyper-for-assignments.git
cd auto-typer
```

**2. Install dependencies:**

```bash
pip install pyautogui pyperclip
```

---

## Usage

**1.** Place your source code file in the project folder (e.g., `code.py`, `code.c`, `code.cpp`).

**2.** Open `auto_typer.py` and set the `CODE_FILE` variable to your file's name:

```python
CODE_FILE = "code.c"   # ← change this everytime for different codes
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
| `CHAR_INTERVAL` | `0.03` | Delay between each character (only used for plain ASCII lines) |
| `LINE_DELAY` | `0.08` | Pause after pressing `Enter` each line |

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
  ├─ Plain ASCII? → type character by character
  ├─ Contains special chars? → copy to clipboard → Ctrl+V
  └─ Press Enter
      │
      ▼
    Done ✅
```

Lines containing only plain ASCII characters (letters, digits, basic punctuation) are typed character by character using `pyautogui.write()`. Lines containing special characters like `{`, `}`, `<`, `>`, `#`, `&`, `|` are injected via the clipboard (`pyperclip` + `Ctrl+V`) to ensure they are typed accurately regardless of keyboard layout. The original clipboard contents are restored after each paste.

---

## Tips & Troubleshooting

** To stop the script immediately:**
- Move your mouse to **any corner of the screen** (PyAutoGUI fail-safe), or
- Press `Ctrl+C` in the terminal window

** Characters being mistyped or skipped?**
- Ensure the file is saved as **UTF-8**
- Increase `CHAR_INTERVAL` slightly (e.g., `0.05`) for plain ASCII lines

** Auto-indent is causing double indentation?**
- Increase `LINE_DELAY` slightly (e.g., `0.1`) to give the editor time to settle after `Enter`
- Turn off auto-indent in the target editor if possible

** Script types in the wrong window?**
- Increase `STARTUP_DELAY` to give yourself more time to click the correct text field

** Clipboard paste not working in the target text box?**
- Some rich-text editors (e.g. TinyMCE in Moodle) may handle `Ctrl+V` differently — try switching the editor to plain-text mode first

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Made with annoyance at moodle using Python & PyAutoGUI</p>