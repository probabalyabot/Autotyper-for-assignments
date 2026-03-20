"""
=====================================================================
  AUTO-TYPER SCRIPT — Windows Edition (Moodle Safe)
=====================================================================

DEPENDENCIES:
  pip install pyautogui keyboard

HOW TO RUN:
  1. Set CODE_FILE to your source file path
  2. Run as Administrator
       Right-click terminal → "Run as administrator"
       python auto_typer.py
  3. Click inside the Moodle text box before countdown ends
  4. Don't touch mouse or keyboard while it runs

STOP: Press Ctrl+C at any time to stop immediately.
      Or move mouse to any screen corner (PyAutoGUI fail-safe).

=====================================================================
"""

import pyautogui
import keyboard
import time
import sys
import os

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────

CODE_FILE     = "code.c"   # <-- Path to your source file
STARTUP_DELAY = 5          # Seconds before typing begins
CHAR_INTERVAL = 0.03       # Seconds between each character
LINE_DELAY    = 0.05       # Seconds to pause after each line break

# Use Shift+Enter instead of Enter to suppress auto-indent in Moodle.
# Set to False for plain textareas.
USE_SHIFT_ENTER = True

# Set to True to convert tabs → spaces before typing.
# Set to False to preserve tabs as-is.
CONVERT_TABS = False
TAB_SIZE     = 4

# Set to True to strip leading whitespace from each line before typing.
# Use when the target editor auto-indents on its own.
STRIP_INDENT = True

# Set to True if the editor auto-closes brackets (e.g. types { and editor
# inserts } automatically). The script will press Delete after each { to
# remove the auto-inserted closing bracket.
AUTO_CLOSE_BRACKETS = True

# ─────────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = True

# Characters that need explicit shift+key combos on a US keyboard layout.
SHIFT_CHARS = {
    '{': '[', '}': ']',
    '(': '9', ')': '0',
    '<': ',', '>': '.',
    '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
    '^': '6', '&': '7', '*': '8',
    '_': '-', '+': '=', '~': '`',
    ':': ';', '"': "'", '?': '/',
    '|': '\\',
}

# Global stop flag
stop_flag = False

def on_ctrl_c():
    global stop_flag
    stop_flag = True

keyboard.add_hotkey("ctrl+c", on_ctrl_c)


def read_file(filepath: str) -> list[str]:
    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: '{filepath}'")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            l = line.rstrip("\n")
            if CONVERT_TABS:
                l = l.replace("\t", " " * TAB_SIZE)
            if STRIP_INDENT:
                l = l.lstrip()
            lines.append(l)

    print(f"[INFO] Loaded '{filepath}' — {len(lines)} lines to type.")
    return lines


def countdown(seconds: int):
    print(f"\n[INFO] Starting in {seconds} seconds — click inside your Moodle text box!\n")
    for i in range(seconds, 0, -1):
        print(f"  Starting in {i}...", end="\r", flush=True)
        time.sleep(1)
    print("  Typing now!              ")


def press_newline():
    if USE_SHIFT_ENTER:
        pyautogui.hotkey("shift", "enter")
    else:
        pyautogui.press("enter")
    time.sleep(LINE_DELAY)


def type_char(char: str):
    """
    Types a single character using the correct method.
    If AUTO_CLOSE_BRACKETS is True, pressing Delete after { removes
    the editor's auto-inserted closing }.
    """
    if char in SHIFT_CHARS:
        pyautogui.hotkey("shift", SHIFT_CHARS[char])
        time.sleep(CHAR_INTERVAL)
        # If editor auto-closes { with }, delete the unwanted auto-inserted }
        if char == '{' and AUTO_CLOSE_BRACKETS:
            time.sleep(0.05)
            pyautogui.press("delete")
            time.sleep(0.05)
    else:
        keyboard.write(char, delay=CHAR_INTERVAL)


def type_line(line: str):
    if line == "":
        return
    for char in line:
        type_char(char)


def auto_type(lines: list[str]):
    global stop_flag
    total = len(lines)

    for index, line in enumerate(lines, start=1):
        if stop_flag:
            print("\n[ABORTED] Stopped by Ctrl+C.")
            sys.exit(0)

        preview = repr(line[:50]) + ("..." if len(line) > 50 else "")
        print(f"  Line {index}/{total}: {preview}")

        type_line(line)

        if index < total:
            press_newline()

    print("\n[DONE] All lines typed successfully!")


def main():
    print("=" * 60)
    print("  AUTO-TYPER — Windows / Moodle Edition")
    print("=" * 60)
    print(f"  Newline mode    : {'Shift+Enter (rich text)' if USE_SHIFT_ENTER else 'Enter (plain textarea)'}")
    print(f"  Tab mode        : {'Convert to ' + str(TAB_SIZE) + ' spaces' if CONVERT_TABS else 'Preserve as-is'}")
    print(f"  Indent mode     : {'Strip leading whitespace' if STRIP_INDENT else 'Preserve indentation'}")
    print(f"  Auto-close fix  : {'On (deletes auto-inserted })' if AUTO_CLOSE_BRACKETS else 'Off'}")
    print(f"  Stop anytime    : Ctrl+C")
    print("=" * 60)

    lines = read_file(CODE_FILE)
    countdown(STARTUP_DELAY)

    try:
        auto_type(lines)
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered (mouse hit screen corner).")
        sys.exit(0)


if __name__ == "__main__":
    main()