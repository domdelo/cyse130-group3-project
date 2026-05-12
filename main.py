# main.py
# Role 1 - Student A
# Responsibility: Title screen, main game loop, and scene routing.
# This file starts the game and connects all modules together.

from engine.game_engine import get_choice
from engine.state import new_state
from security.security import log_event, save_game, load_game
from content.story import (
    scene_opening,
    scene_ranger_station,
    scene_perimeter,
    scene_deep_woods,
    scene_abandoned_tent,
    scene_old_firepit,
    scene_ending,
)

# =====================
# TITLE SCREEN
# =====================

def show_title():
    """Print the game title and instructions before play begins."""
    print("=" * 50)
    print("       THE CURSED CAMPGROUND")
    print("      A Horror / Mystery Adventure")
    print("=" * 50)
    print()
    print("  People have been disappearing at Campground 7.")
    print("  You just arrived. Your phone has no signal.")
    print("  The other sites are empty.")
    print("  Something is very wrong.")
    print()
    print("  HOW TO PLAY")
    print("  - Type a number and press Enter to choose.")
    print("  - Collect items and talk to everyone you meet.")
    print("  - Your choices decide your ending.")
    print("  - There are 3 story paths and 3 possible endings.")
    print()
    print("=" * 50)
    print()

# =====================
# START MENU
# =====================

def show_start_menu():
    """
    Show the start menu and return the starting game state.
    Player can start a new game, load a saved game, or quit.
    """
    print("  What would you like to do?\n")
    choice = get_choice(["New game", "Load saved game", "Quit"])

    if choice == 0:
        # Fresh state for a new game
        return new_state()
    elif choice == 1:
        # load_game() returns None if no save exists or if tampered
        loaded = load_game()
        if loaded is not None:
            return loaded
        # If load failed, fall back to a new game automatically
        print("  Starting a new game instead.\n")
        return new_state()
    else:
        return None  # Signal to quit before the loop starts

# =====================
# SCENE ROUTING TABLE
# =====================

# Maps each scene name (string) to its scene function (from story.py).
# The main loop looks up the current scene name here and calls it.
# To add a new scene: add one line to this dictionary.

SCENES = {
    "opening":        scene_opening,
    "ranger_station": scene_ranger_station,
    "perimeter":      scene_perimeter,
    "deep_woods":     scene_deep_woods,
    "abandoned_tent": scene_abandoned_tent,
    "old_firepit":    scene_old_firepit,
    "ending":         scene_ending,
}

# =====================
# MAIN GAME LOOP
# =====================

def main():
    """
    Entry point for The Cursed Campground.
    Shows the title, handles the start menu, then runs the main loop.
    Each iteration: call the current scene, get back the next scene name, repeat.
    """
    show_title()
    log_event("GAME_START", "New session")

    # Get starting state from the start menu
    state = show_start_menu()

    # If player chose Quit from the start menu, exit cleanly
    if state is None:
        print("\n  Goodbye.\n")
        log_event("GAME_END", "Quit at start menu")
        return

    # Start at the opening scene
    current_scene = "opening"

    # Main loop — keeps running until the game ends or player quits
    while current_scene not in ("quit", "done"):

        if current_scene in SCENES:
            # Call the scene function, it returns the next scene name
            next_scene = SCENES[current_scene](state)
            current_scene = next_scene
        else:
            # Safety net: unknown scene name — log it and go back to opening
            log_event("ERROR", f"Unknown scene: {current_scene}")
            print(f"\n  [ Something went wrong. Returning to camp. ]\n")
            current_scene = "opening"

        # Once the ending scene is reached, run it and stop the loop
        if current_scene == "ending":
            scene_ending(state)
            current_scene = "done"

    print("  [ Game over. Thanks for playing! ]\n")

# =====================
# ENTRY POINT
# =====================

if __name__ == "__main__":
    main()
