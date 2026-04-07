"""
=====================================================================
  AUTO-TYPER SCRIPT — macOS Edition (Moodle Safe)
=====================================================================

DEPENDENCIES:
  pip install pynput

ACCESSIBILITY PERMISSION REQUIRED:
  macOS requires accessibility access for keyboard control.
  Go to: System Settings → Privacy & Security → Accessibility
  Add your Terminal (or IDE) to the allowed apps.

HOW TO RUN:
  1. Set CODE_FILE to your source file path
  2. Run the script:
       python auto_typer_mac.py
  3. Click inside the Moodle text box before the countdown ends
  4. Don't touch mouse or keyboard while it runs

STOP: Press Ctrl+C in the terminal at any time.
      Or move the mouse to any screen corner (PyAutoGUI fail-safe).

=====================================================================
"""

import time
import sys
import os
import threading

import pyautogui
from pynput.keyboard import Key, Controller, Listener

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
CONVERT_TABS = False
TAB_SIZE     = 4

# Set to True to strip leading whitespace from each line before typing.
STRIP_INDENT = True

# Set to True if the editor auto-closes brackets (types { and editor
# inserts } automatically). The script will press Delete after { to
# remove the auto-inserted closing bracket.
AUTO_CLOSE_BRACKETS = True

# ─────────────────────────────────────────────────────────────────────

pyautogui.FAILSAFE = True

keyboard = Controller()

# Global stop flag
stop_flag = False

# ─────────────────────────────────────────────────────────────────────
# Ctrl+C stop listener (runs in background thread)
# ─────────────────────────────────────────────────────────────────────

_ctrl_held = False

def _on_press(key):
    global _ctrl_held, stop_flag
    if key in (Key.ctrl_l, Key.ctrl_r):
        _ctrl_held = True
    try:
        if _ctrl_held and key.char == 'c':
            stop_flag = True
    except AttributeError:
        pass

def _on_release(key):
    global _ctrl_held
    if key in (Key.ctrl_l, Key.ctrl_r):
        _ctrl_held = False

listener_thread = Listener(on_press=_on_press, on_release=_on_release)
listener_thread.daemon = True
listener_thread.start()

# ─────────────────────────────────────────────────────────────────────

# Characters that require Shift on a US keyboard layout.
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
        with keyboard.pressed(Key.shift):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
    else:
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    time.sleep(LINE_DELAY)


def type_char(char: str):
    """
    Types a single character using pynput.
    Handles shifted characters and optional bracket auto-close deletion.
    """
    if char in SHIFT_CHARS:
        with keyboard.pressed(Key.shift):
            keyboard.press(SHIFT_CHARS[char])
            keyboard.release(SHIFT_CHARS[char])
        time.sleep(CHAR_INTERVAL)
        if char == '{' and AUTO_CLOSE_BRACKETS:
            time.sleep(0.05)
            keyboard.press(Key.delete)
            keyboard.release(Key.delete)
            time.sleep(0.05)
    else:
        # pynput type() handles unicode characters cleanly on macOS
        keyboard.type(char)
        time.sleep(CHAR_INTERVAL)


def type_line(line: str):
    if line == "":
        return
    for char in line:
        if stop_flag:
            return
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

        if stop_flag:
            print("\n[ABORTED] Stopped by Ctrl+C.")
            sys.exit(0)

        if index < total:
            press_newline()

    print("\n[DONE] All lines typed successfully!")


def main():
    print("=" * 60)
    print("  AUTO-TYPER — macOS / Moodle Edition")
    print("=" * 60)
    print(f"  Newline mode    : {'Shift+Enter (rich text)' if USE_SHIFT_ENTER else 'Enter (plain textarea)'}")
    print(f"  Tab mode        : {'Convert to ' + str(TAB_SIZE) + ' spaces' if CONVERT_TABS else 'Preserve as-is'}")
    print(f"  Indent mode     : {'Strip leading whitespace' if STRIP_INDENT else 'Preserve indentation'}")
    print(f"  Auto-close fix  : {'On (deletes auto-inserted })' if AUTO_CLOSE_BRACKETS else 'Off'}")
    print(f"  Stop anytime    : Ctrl+C (terminal) or mouse to screen corner")
    print("=" * 60)

    lines = read_file(CODE_FILE)
    countdown(STARTUP_DELAY)

    try:
        auto_type(lines)
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered (mouse hit screen corner).")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[ABORTED] Stopped by Ctrl+C.")
        sys.exit(0)


if __name__ == "__main__":
    main()