# engine/game_engine.py
# Role 1 - Student A
# Responsibility: Menu display and safe input handling.
# This module is used by main.py and by every scene in story.py.
# It is the ONLY place in the project where player input is read,
# so all input validation lives here in one spot.

from security.security import log_event

# =====================
# MENU + INPUT
# =====================

def get_choice(options):
    """
    Display a numbered menu and return the player's choice safely.

    Shows each option with a number. Keeps asking until the player
    types a valid number in range. Never crashes on bad input.

    Parameters:
        options (list) : List of strings, one per menu option.

    Returns:
        int : The player's choice as a 0-based index.
              (Player types 1, function returns 0. Player types 2, returns 1. Etc.)

    Example:
        choice = get_choice(["Go north", "Go south", "Check inventory"])
        # Player types 2  ->  choice == 1  ->  "Go south"
    """
    print()
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        try:
            raw = input("\n  Enter a number: ").strip()
            choice = int(raw)

            if 1 <= choice <= len(options):
                log_event("CHOICE_MADE", f"Choice={choice}/{len(options)}")
                return choice - 1   # Convert to 0-based index

            # Number typed but out of range
            print(f"  Invalid choice. Please enter a number from 1 to {len(options)}.")
            log_event("INPUT_INVALID", f"Out of range: {raw}")

        except ValueError:
            # Player typed letters or symbols instead of a number
            print("  Please type a number, not letters.")
            log_event("INPUT_INVALID", "Non-numeric input")


def get_text_answer(prompt):
    """
    Ask the player a free-text question and return their answer.

    Used for puzzle challenges where the player types a word answer
    rather than picking from a numbered menu.

    Parameters:
        prompt (str) : The question to show the player.

    Returns:
        str : The player's answer, stripped of whitespace and lowercased.
    """
    while True:
        try:
            raw = input(f"  {prompt} ").strip()
            if raw == "":
                print("  Please type something.")
            else:
                return raw.lower()
        except ValueError:
            print("  Something went wrong. Please try again.")


# =====================
# DISPLAY HELPERS
# =====================

def print_header(title):
    """
    Print a formatted section header for a scene or event.

    Parameters:
        title (str) : The scene or event name to display.

    Example output:
        ==================================================
          --- RANGER STATION ---
        ==================================================
    """
    print("\n" + "=" * 50)
    print(f"  --- {title} ---")
    print("=" * 50)


def pause():
    """
    Pause the game until the player presses Enter.
    Used at the end of NPC dialogues and story beats.
    """
    input("\n  [ Press Enter to continue... ]")
