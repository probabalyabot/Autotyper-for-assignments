"""
=====================================================================
  AUTO-TYPER SCRIPT FOR MOODLE VPL (CODEMIRROR EDITOR)
=====================================================================

DEPENDENCIES:
  Install required libraries via pip:
    pip install pyautogui keyboard

HOW TO RUN:
  1. Save your code in a file (e.g., code.c, code.cpp, code.py, etc.)
  2. Open a terminal (may require Administrator/Elevated privileges for
     the global keyboard hooks to work correctly) and run:
       python auto_typer.py
  3. When prompted, click inside the VPL CodeMirror editor.
  4. The script will begin typing automatically.

CODEMIRROR WORKAROUND:
  Moodle VPL uses CodeMirror, which intercepts Enter presses and 
  automatically adds smart indentation based on syntax.
  To prevent compounding indentation, this script:
    - Presses Enter
    - Instantly presses Ctrl+Z to undo CodeMirror's auto-indent
    - Types the line's exact leading spaces using spacebar presses
    - Types the rest of the line's content

NOTES:
  - Do NOT move your mouse or type anything while the script is running.
  - Press ESC at any time to globally abort the script.
  - Tabs are automatically converted to 4 spaces.

=====================================================================
"""

import pyautogui
import keyboard
import time
import sys
import os

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION — Adjust these values to your needs
# ─────────────────────────────────────────────────────────────────────

# Path to the source code file you want to type out
CODE_FILE = "code.c"  # <-- Change this to your file path

# Delay (in seconds) before typing begins.
STARTUP_DELAY = 5  # seconds

# Delay between each individual character being typed (in seconds).
CHAR_INTERVAL = 0.03  # seconds

# Delay (in seconds) after pressing Enter at the end of each line.
LINE_DELAY = 0.05  # seconds

# Global emergency stop key
PANIC_KEY = "esc"

# ─────────────────────────────────────────────────────────────────────
# SAFETY SETTING
pyautogui.FAILSAFE = True

# Global termination flag
abort_typing = False

def emergency_stop():
    global abort_typing
    abort_typing = True

# Register the global abort hotkey
keyboard.add_hotkey(PANIC_KEY, emergency_stop)


def read_file(filepath: str) -> list[str]:
    """
    Reads the source code file and returns a list of lines.
    Tabs are converted to 4 spaces to prevent indentation issues.
    """
    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: '{filepath}'")
        print("  Please check the CODE_FILE path at the top of the script.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        # Replace all tab characters with 4 spaces to normalize indentation
        lines = [line.rstrip("\n").replace("\t", "    ") for line in f]

    print(f"[INFO] Loaded '{filepath}' — {len(lines)} lines to type.")
    return lines


def countdown(seconds: int):
    """
    Displays a countdown in the terminal.
    """
    print(f"\n[INFO] Starting in {seconds} seconds — click inside your target text box now!\n")
    for i in range(seconds, 0, -1):
        if abort_typing:
            print("\n[ABORTED] Script interrupted by user before typing began.")
            sys.exit(0)
        print(f"  Starting in {i}...", end="\r", flush=True)
        time.sleep(1)
    print("  Typing now!              ")


def auto_type(lines: list[str], interval: float, line_delay: float):
    """
    Main typing loop optimized for CodeMirror editors.
    """
    total = len(lines)

    for index, line in enumerate(lines, start=1):
        if abort_typing:
            print("\n\n[ABORTED] Emergency stop triggered inside typing loop!")
            sys.exit(0)

        print(f"  Typing line {index}/{total}: {repr(line[:40])}{'...' if len(line) > 40 else ''}")

        # 1. Separate leading whitespace and actual code
        stripped_line = line.lstrip(' ')
        leading_spaces = len(line) - len(stripped_line)

        # 2. Explicitly type leading spaces to ensure consistent indent mapping
        if leading_spaces > 0:
            for _ in range(leading_spaces):
                if abort_typing: break
                pyautogui.press("space")
                time.sleep(0.005) # Tiny pause to ensure browser registers the space

        # 3. Type the rest of the line's content
        if stripped_line:
            pyautogui.write(stripped_line, interval=interval)

        # 4. Handle newline and the CodeMirror auto-indent behavior
        if index < total:
            pyautogui.press("enter")
            
            # Wait a split second to allow CodeMirror's event listener to fire and insert auto-indent
            time.sleep(0.1)
            
            # Clear any auto-indentation inserted by CodeMirror.
            # We type a dummy character 'x', select back to column 0, and delete it.
            # This safely throws away the editor's smart indentation without deleting the newline itself.
            # (Ctrl+Z fails here because it undoes both the auto-indent AND the newline)
            pyautogui.write("x")
            pyautogui.hotkey("shift", "home")
            pyautogui.hotkey("shift", "home")  # Multiple presses ensure we go past indent to column 0
            pyautogui.hotkey("shift", "home")
            pyautogui.press("backspace")
            
            # Pause before typing the next line
            time.sleep(line_delay)

    if not abort_typing:
        print("\n[DONE] All lines have been typed successfully!")


def main():
    print("=" * 60)
    print("  AUTO-TYPER FOR MOODLE VPL (CODEMIRROR)")
    print("=" * 60)

    # Read the file
    lines = read_file(CODE_FILE)

    # Show countdown
    countdown(STARTUP_DELAY)

    # Begin typing
    try:
        auto_type(lines, CHAR_INTERVAL, LINE_DELAY)
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered! Mouse moved to a screen corner.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[ABORTED] Script interrupted by user (Ctrl+C).")
        sys.exit(0)


if __name__ == "__main__":
    main()
