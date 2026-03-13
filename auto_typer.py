"""
=====================================================================
  AUTO-TYPER SCRIPT — Simulates Human Typing Using PyAutoGUI
=====================================================================

DEPENDENCIES:
  Install required libraries via pip:
    pip install pyautogui

HOW TO RUN:
  1. Save your code in a file (e.g., code.c, code.cpp, code.py, etc.)
  2. Open a terminal and run:
       python auto_typer.py
  3. When prompted (or after the startup delay), click inside the
     target text box / code editor where you want the code typed.
  4. The script will begin typing automatically.

NOTES:
  - Do NOT move your mouse or type anything while the script is running.
  - Press Ctrl+C in the terminal to abort at any time.
  - Tabs are automatically converted to 4 spaces.
  - The script types line-by-line and presses Enter after each line.

=====================================================================
"""

import pyautogui
import time
import sys
import os

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION — Adjust these values to your needs
# ─────────────────────────────────────────────────────────────────────

# Path to the source code file you want to type out
CODE_FILE = "code.c"  # <-- Change this to your file path

# Delay (in seconds) before typing begins.
# Use this time to click into the target text box.
STARTUP_DELAY = 5  # seconds

# Delay between each individual character being typed (in seconds).
# Lower = faster, Higher = more human-like.
# Recommended range: 0.02 (fast) to 0.08 (normal human pace)
CHAR_INTERVAL = 0.03  # seconds

# Delay (in seconds) after pressing Enter at the end of each line.
# Helps prevent race conditions with auto-indent in some editors.
LINE_DELAY = 0.05  # seconds

# ─────────────────────────────────────────────────────────────────────
# SAFETY SETTING
# PyAutoGUI will raise an exception if the mouse hits a screen corner.
# This acts as a fail-safe to stop the script if needed.
# To disable: set pyautogui.FAILSAFE = False (not recommended)
# ─────────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = True


def read_file(filepath: str) -> list[str]:
    """
    Reads the source code file and returns a list of lines.
    Tabs are converted to 4 spaces to prevent indentation issues.
    The file is read with UTF-8 encoding for broad character support.
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
    Displays a countdown in the terminal so the user knows
    how much time is left before typing begins.
    """
    print(f"\n[INFO] Starting in {seconds} seconds — click inside your target text box now!\n")
    for i in range(seconds, 0, -1):
        print(f"  Starting in {i}...", end="\r", flush=True)
        time.sleep(1)
    print("  Typing now!              ")  # Overwrite the countdown line


def type_line(line: str, interval: float):
    """
    Types a single line of text character by character using PyAutoGUI.

    Why not use pyautogui.write()?
      pyautogui.write() has known issues with special characters on
      non-US keyboard layouts and can drop characters like {, }, <, >,
      #, @, etc. Using pyautogui.typewrite() with 'interval' works for
      simple ASCII, but for full Unicode and special character support,
      we use pyautogui.write() carefully combined with hotkey for symbols.

    The safest approach for special characters is pyautogui.write()
    with the message parameter which handles Unicode strings properly,
    combined with a per-character interval.
    """
    if line == "":
        # Empty line — just press Enter (handled by caller)
        return

    # pyautogui.write() handles standard printable ASCII characters well.
    # For maximum compatibility with special chars on Windows, we type
    # the entire line as a string with an interval between each character.
    pyautogui.write(line, interval=interval)


def auto_type(lines: list[str], interval: float, line_delay: float):
    """
    Main typing loop.
    Iterates over each line, types it out character by character,
    then presses Enter to move to the next line.
    """
    total = len(lines)

    for index, line in enumerate(lines, start=1):
        print(f"  Typing line {index}/{total}: {repr(line[:40])}{'...' if len(line) > 40 else ''}")

        # Type the current line content
        type_line(line, interval)

        # Press Enter to go to the next line in the editor
        pyautogui.press("enter")

        # Small pause after Enter to let the editor settle
        # (prevents issues with auto-indent firing too slowly)
        time.sleep(line_delay)

    print("\n[DONE] All lines have been typed successfully!")


def main():
    """
    Entry point of the script.
    Reads the file, runs the countdown, then begins typing.
    """
    print("=" * 60)
    print("  AUTO-TYPER — PyAutoGUI Code Typing Script")
    print("=" * 60)

    # Step 1: Read the source file into a list of lines
    lines = read_file(CODE_FILE)

    # Step 2: Show countdown so user has time to focus the target text box
    countdown(STARTUP_DELAY)

    # Step 3: Begin typing the code line by line
    try:
        auto_type(lines, CHAR_INTERVAL, LINE_DELAY)
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered! Mouse moved to a screen corner.")
        print("  Script stopped to prevent unintended input.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[ABORTED] Script interrupted by user (Ctrl+C).")
        sys.exit(0)


if __name__ == "__main__":
    main()
