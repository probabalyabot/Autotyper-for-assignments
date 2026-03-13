"""
=====================================================================
  AUTO-TYPER SCRIPT — Simulates Human Typing Using PyAutoGUI
=====================================================================

DEPENDENCIES:
  Install required libraries via pip:
    pip install pyautogui pyperclip

HOW TO RUN:
  1. Save your code in a file (e.g., code.c, code.cpp, code.py, etc.)
  2. Open a terminal and run:
       python auto_typer.py
  3. When prompted, click inside the target text box / editor.
  4. The script will begin typing automatically.

NOTES:
  - Do NOT move your mouse or type anything while the script is running.
  - Press Ctrl+C in the terminal to abort at any time.
  - Move mouse to any screen corner to emergency-stop (PyAutoGUI failsafe).
  - Special characters like { } < > # @ are handled correctly via clipboard.

=====================================================================
"""

import pyautogui
import pyperclip
import time
import sys
import os

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────

CODE_FILE     = "code.c"   # <-- Path to your source file
STARTUP_DELAY = 5          # Seconds before typing begins (use to click into target)
LINE_DELAY    = 0.08       # Seconds to pause after each Enter keypress
CHAR_INTERVAL = 0.03       # Seconds between chars (only used for safe ASCII fallback)

# ─────────────────────────────────────────────────────────────────────
pyautogui.FAILSAFE = True  # Move mouse to top-left corner to emergency stop


# Characters that pyautogui.write() handles safely on all keyboards.
# Everything outside this set will be typed via clipboard to avoid corruption.
SAFE_CHARS = set(
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    " .,;:'\"!?-_="
)


def read_file(filepath: str) -> list[str]:
    if not os.path.isfile(filepath):
        print(f"[ERROR] File not found: '{filepath}'")
        print("  Check the CODE_FILE path at the top of the script.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n").replace("\t", "    ") for line in f]

    print(f"[INFO] Loaded '{filepath}' — {len(lines)} lines to type.")
    return lines


def countdown(seconds: int):
    print(f"\n[INFO] Starting in {seconds} seconds — click inside your target text box!\n")
    for i in range(seconds, 0, -1):
        print(f"  Starting in {i}...", end="\r", flush=True)
        time.sleep(1)
    print("  Typing now!              ")


def type_line(line: str):
    """
    Types a single line using the safest method per segment:
      - Pure safe-ASCII runs → pyautogui.write() (character by character)
      - Any line containing special chars → clipboard paste (Ctrl+V)

    Clipboard paste is instant and 100% accurate for all Unicode/special chars.
    We restore the original clipboard content afterward.
    """
    if line == "":
        return  # Empty line, caller handles Enter

    # Check if the whole line is safe ASCII
    if all(c in SAFE_CHARS for c in line):
        pyautogui.write(line, interval=CHAR_INTERVAL)
    else:
        # Save current clipboard, paste line, restore clipboard
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            original_clipboard = ""

        pyperclip.copy(line)
        time.sleep(0.05)  # Let clipboard settle
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.05)

        # Restore clipboard
        try:
            pyperclip.copy(original_clipboard)
        except Exception:
            pass


def auto_type(lines: list[str], line_delay: float):
    total = len(lines)

    for index, line in enumerate(lines, start=1):
        preview = repr(line[:50]) + ("..." if len(line) > 50 else "")
        print(f"  Line {index}/{total}: {preview}")

        type_line(line)

        pyautogui.press("enter")
        time.sleep(line_delay)

    print("\n[DONE] All lines typed successfully!")


def main():
    print("=" * 60)
    print("  AUTO-TYPER — Special Character Safe Edition")
    print("=" * 60)

    lines = read_file(CODE_FILE)
    countdown(STARTUP_DELAY)

    try:
        auto_type(lines, LINE_DELAY)
    except pyautogui.FailSafeException:
        print("\n[ABORTED] Fail-safe triggered (mouse hit screen corner).")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n[ABORTED] Stopped by user (Ctrl+C).")
        sys.exit(0)


if __name__ == "__main__":
    main()