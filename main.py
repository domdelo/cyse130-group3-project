# main.py
# CyberScape: The Cursed Campground
# Role 1 - Dagmawi Debasu
# Responsibility: Title screen, main game loop, and scene routing.
# This file starts the game and runs the main loop.
# It works with the dictionary-based story.py (scenes = { "start": {...}, ... })

from engine.game_engine import get_choice, print_header, pause
from engine.state import create_new_state, game_is_over, print_state_summary
from security.security import log_event
from security.save_load import save_game, load_game
from content.story import scenes, get_available_choices
from content.npcs import ranger_npc, kid_npc, scientist_npc, guard_npc, ghost_npc
from systems.challenges import challenge_rangers_cipher, challenge_shadow_encounter


# =====================
# TITLE SCREEN
# =====================

def show_title():
    # Prints the game title and instructions before play begins
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
    # Shows the start menu and returns the starting game state
    # Returns None if the player chose to quit

    print("  What would you like to do?\n")
    choice = get_choice(["New game", "Load saved game", "Quit"])

    if choice == 0:
        # Brand new game - fresh state
        return create_new_state()

    elif choice == 1:
        # Try to load a saved game
        loaded = load_game()
        if loaded is not None:
            return loaded
        # Load failed (no file or tampered) - start fresh
        print("  Starting a new game instead.\n")
        return create_new_state()

    else:
        # Player chose quit
        return None


# =====================
# RUN SCENE EFFECTS
# =====================

def run_scene_effect(scene, state):
    # Some scenes in story.py have an "effect" key with a lambda function
    # This runs that lambda to update the state
    # Example: "effect": lambda state: state.update({"met_ranger": True})

    if "effect" in scene:
        scene["effect"](state)


# =====================
# CHECK FOR NPC
# =====================

def run_npc_for_scene(scene_key, state):
    # Some scenes trigger an NPC interaction
    # This maps scene names to their NPC functions from npcs.py

    npc_map = {
        "ranger_scene":    ranger_npc,
        "kid_scene":       kid_npc,
        "journal_scene":   scientist_npc,
        "ghost_scene":     ghost_npc,
    }

    if scene_key in npc_map:
        npc_map[scene_key](state)
        pause()


# =====================
# CHECK FOR CHALLENGE
# =====================

def run_challenge_for_scene(scene_key, state):
    # Some scenes trigger a challenge from challenges.py
    # Returns updated state after the challenge runs

    if scene_key == "challenge_scene":
        # The cipher puzzle runs before the ghost question
        if state["challenge_cipher_result"] == "":
            state = challenge_rangers_cipher(state)

        # The shadow encounter runs when confronting the ghost
        state = challenge_shadow_encounter(state)

    return state


# =====================
# HANDLE SAVE
# =====================

def offer_save(state):
    # Asks the player if they want to save after major scenes
    print()
    print("  Would you like to save your progress?")
    choice = get_choice(["Yes, save the game", "No, keep going"])
    if choice == 0:
        save_game(state)
    print()


# =====================
# DISPLAY SCENE
# =====================

def display_scene(scene_key, state):
    # Prints the scene text and returns the player's chosen next scene key
    # This is the core of the game loop

    # Get the scene dictionary from story.py
    scene = scenes[scene_key]

    # Print the scene header and text
    print_header(scene_key.replace("_", " ").upper())
    print()
    print("  " + scene["text"])
    print()

    # Log that the player entered this scene
    log_event("CHOICE_MADE", details="Scene=" + scene_key)

    # Run any effect the scene has (updates flags in state)
    run_scene_effect(scene, state)

    # Run NPC for this scene if there is one
    run_npc_for_scene(scene_key, state)

    # Run challenge for this scene if there is one
    state = run_challenge_for_scene(scene_key, state)

    # Check if this is an ending scene - no choices needed
    if scene.get("end") == True:
        pause()
        return "done"

    # Get valid choices (filters out ones with unmet conditions)
    valid_choices = get_available_choices(scene, state)

    # If there are no choices left something went wrong - go back to start
    if len(valid_choices) == 0:
        print("  [ No choices available. Returning to camp... ]")
        log_event("ERROR", details="Scene=" + scene_key + " NoChoicesAvailable")
        return "start"

    # Build a list of choice descriptions to show the player
    choice_labels = []
    for c in valid_choices:
        choice_labels.append(c["desc"])

    # Show the menu and get the player's pick
    picked = get_choice(choice_labels)

    # Return the next scene key from the chosen choice
    next_scene = valid_choices[picked]["next"]
    log_event("CHOICE_MADE", details="Scene=" + scene_key + " Next=" + next_scene)

    return next_scene


# =====================
# MAIN GAME LOOP
# =====================

def main():
    # Entry point - shows title, start menu, then runs the game loop

    show_title()
    log_event("GAME_START", details="New session started")

    # Get starting state from the start menu
    state = show_start_menu()

    # Player chose quit at the start menu
    if state is None:
        print("\n  Goodbye.\n")
        log_event("GAME_END", details="Quit at start menu")
        return

    # Always start at the "start" scene (matches story.py key)
    current_scene = "start"

    # Main loop - keeps going until game ends or player quits
    while current_scene not in ("done", "quit"):

        # Make sure the scene key exists in the story dictionary
        if current_scene not in scenes:
            log_event("ERROR", details="UnknownScene=" + current_scene)
            print("\n  [ Something went wrong. Returning to camp. ]\n")
            current_scene = "start"
            continue

        # Display the scene and get the next scene key back
        next_scene = display_scene(current_scene, state)

        # Offer a save after certain key scenes
        save_scenes = ["ranger_scene", "kid_scene", "journal_scene"]
        if current_scene in save_scenes:
            offer_save(state)

        # Check if the player has died or reached an ending
        if game_is_over(state):
            next_scene = "done"

        current_scene = next_scene

    # Game is finished
    print()
    print("  [ Game over. Thanks for playing The Cursed Campground! ]")
    print()
    log_event("GAME_END", details="Session ended")


# =====================
# ENTRY POINT
# =====================

if __name__ == "__main__":
    main()
