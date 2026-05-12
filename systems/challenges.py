# systems/challenges.py
# CyberScape: The Cursed Campground
# Cyber Role: Dom DeLeat
# This file has the two required challenges:
#   Challenge 1 - The Ranger's Cipher (a decoding puzzle)
#   Challenge 2 - The Shadow Encounter (a combat encounter)

import random

from security.security import log_event, get_int_choice, get_text_input


# ==================================================
# CHALLENGE 1 - THE RANGER'S CIPHER
# Location: Ranger Station
#
# The player finds a note with a coded word.
# They must decode it using a Caesar cipher (shift each letter back by 3).
# Coded word:  I L U H Z R R G
# Answer:      F I R E W O O D
#
# Success: Player gets the Master Key item + a clue about the curse
# Failure: An alarm is triggered (makes later scenes harder)
# ==================================================

# The correct answer the player needs to figure out
CIPHER_ANSWER = "FIREWOOD"

# How many wrong guesses before failing
MAX_ATTEMPTS = 3

# The note the player finds
CIPHER_NOTE = """
You find a dusty note pinned to the ranger station door:

  'If you're reading this, I may be gone.
   The password is encoded below.
   Shift each letter BACK by 3 in the alphabet to decode it.
   (Example: D becomes A,  E becomes B,  F becomes C)

   Coded word:  I L U H Z R R G

   Unlock the shed. Take what you need. Trust no one after dark.'
                              - Ranger Holt
"""


def challenge_rangers_cipher(state):
    # Runs the cipher puzzle
    # state = the game state dictionary
    # Returns the updated game state

    print("\n============================================================")
    print("  CHALLENGE: The Ranger's Cipher")
    print("============================================================")
    print(CIPHER_NOTE)
    print("  Decode the note and type the password to unlock the shed.")
    print("  You have " + str(MAX_ATTEMPTS) + " attempts.\n")

    log_event("CHALLENGE_ATTEMPT", details="Puzzle=RangersCipher START")

    attempts_used = 0

    while attempts_used < MAX_ATTEMPTS:
        attempts_used = attempts_used + 1

        player_answer = get_text_input("  Attempt " + str(attempts_used) + "/" + str(MAX_ATTEMPTS) + " - Enter the password: ")

        # Clean up what they typed: remove spaces, make all caps
        player_answer = player_answer.strip().upper().replace(" ", "")

        # Check if they got it right
        if player_answer == CIPHER_ANSWER:
            print("\n  Correct! The padlock clicks open.")
            print("  Inside the shed you find a MASTER KEY and a torn journal page")
            print("  with coordinates to the cursed circle.\n")

            log_event("CHALLENGE_ATTEMPT", "SUCCESS", "Puzzle=RangersCipher Attempts=" + str(attempts_used))

            # Add the Master Key to the player's inventory if they don't have it
            if "Master Key" not in state["inventory"]:
                state["inventory"].append("Master Key")

            # Set flags so the rest of the game knows this challenge was completed
            state["challenge_cipher_result"] = "success"
            state["has_cipher_clue"] = True

            return state

        else:
            # Wrong answer
            attempts_left = MAX_ATTEMPTS - attempts_used
            log_event("CHALLENGE_ATTEMPT", "FAIL", "Puzzle=RangersCipher Attempts=" + str(attempts_used))

            if attempts_left > 0:
                print("  Wrong password. " + str(attempts_left) + " attempt(s) remaining.\n")
            else:
                print("\n  Wrong again. You've used all your attempts.")
                print("  A loud CLANG echoes through the campground.")
                print("  Something in the woods heard you...\n")

    # If we get here, the player used all attempts and never got it right
    state["challenge_cipher_result"] = "fail"
    state["alarm_triggered"] = True   # This flag makes later scenes harder

    return state


# ==================================================
# CHALLENGE 2 - THE SHADOW ENCOUNTER
# Location: The Cursed Circle
#
# A ghostly figure blocks the path to the ritual site.
# The player picks a strategy: Fight, Distract, or Flee.
# Combat uses random dice rolls (1-6). Items boost your damage.
#
# Item bonuses:
#   Holy Water    = +3 damage
#   Silver Compass = +2 damage
#   Ranger's Torch = +1 damage
#
# Success: Path to the ritual site is open
# Failure: Player dies and gets the "become part of curse" ending
# ==================================================

# Ghost starts with 3 HP. Player deals 1 base damage per round + item bonuses.
GHOST_STARTING_HP = 3
PLAYER_BASE_DAMAGE = 1

# Items that give extra damage and how much bonus they provide
ITEM_DAMAGE_BONUSES = {
    "Holy Water": 3,
    "Silver Compass": 2,
    "Ranger's Torch": 1
}


def get_item_bonus(inventory):
    # Looks through the player's inventory and totals up any damage bonuses
    # inventory = list of item name strings
    # Returns the total bonus as a number

    total_bonus = 0

    for item in inventory:
        if item in ITEM_DAMAGE_BONUSES:
            total_bonus = total_bonus + ITEM_DAMAGE_BONUSES[item]

    return total_bonus


def challenge_shadow_encounter(state):
    # Runs the Shadow Encounter combat/obstacle
    # state = the game state dictionary
    # Returns the updated game state

    print("\n============================================================")
    print("  CHALLENGE: The Shadow Encounter")
    print("============================================================")
    print("\n  You step into the Cursed Circle. Fog swirls at your ankles.")
    print("  A dark shape rises from the ground - the ghostly figure.")
    print("  Its hollow eyes lock onto you.")
    print("  It will NOT let you pass without a fight.\n")

    # Get inventory from state (use empty list if inventory key doesn't exist)
    inventory = state["inventory"]

    # Calculate item bonus
    item_bonus = get_item_bonus(inventory)

    # Tell the player about any bonuses they have
    if item_bonus > 0:
        print("  Your items give you a +" + str(item_bonus) + " damage bonus!")
        for item in inventory:
            if item in ITEM_DAMAGE_BONUSES:
                print("    - " + item + ": +" + str(ITEM_DAMAGE_BONUSES[item]))
        print()

    log_event("CHALLENGE_ATTEMPT", details="Encounter=ShadowEncounter START")

    # Show the player their options
    print("  What do you do?")
    print("    1. FIGHT  - Attack the shadow with everything you have")
    print("    2. DISTRACT - Throw something to lure it away and slip past")
    print("    3. FLEE   - Run back to the campfire (gives up this encounter)")
    print()

    strategy = get_int_choice("  Enter choice (1-3): ", 1, 3, scene="cursed_circle")

    # ---- OPTION 3: FLEE ----
    if strategy == 3:
        print("\n  You turn and run back toward the campfire.")
        print("  The shadow shrieks but cannot cross the firelight.")
        print("  You are safe for now, but the ritual site is still blocked.\n")
        log_event("CHALLENGE_ATTEMPT", "FAIL", "Encounter=ShadowEncounter Fled")
        state["challenge_shadow_result"] = "fled"
        return state

    # ---- OPTION 2: DISTRACT ----
    if strategy == 2:
        dice_roll = random.randint(1, 6)
        print("\n  You hurl a rock into the darkness... (Dice roll: " + str(dice_roll) + ")")

        if dice_roll >= 4:
            print("  The shadow spins toward the noise. You dash past it!")
            print("  You have made it through to the ritual site!\n")
            log_event("CHALLENGE_ATTEMPT", "SUCCESS", "Encounter=ShadowEncounter Distracted")
            state["challenge_shadow_result"] = "success"
            return state
        else:
            print("  The shadow ignores the sound. It knows it is a trick.")
            print("  It charges at you. Now you have to fight!\n")
            # No return here - the code falls through into the FIGHT section below

    # ---- OPTION 1: FIGHT (also handles a failed distract) ----
    print("  You stand your ground and attack the shadow!\n")

    ghost_hp = GHOST_STARTING_HP
    player_hp = state["player_health"]
    combat_round = 0

    # Keep fighting until the ghost is defeated or the player dies
    while ghost_hp > 0 and player_hp > 0:
        combat_round = combat_round + 1

        # Player attacks
        dice_roll = random.randint(1, 6)
        damage = PLAYER_BASE_DAMAGE + item_bonus

        # A high roll adds 1 extra damage (lucky hit)
        if dice_roll >= 5:
            damage = damage + 1

        ghost_hp = ghost_hp - damage

        print("  Round " + str(combat_round) + ": You roll a " + str(dice_roll) + ".")
        print("  You deal " + str(damage) + " damage. Ghost HP: " + str(max(ghost_hp, 0)))

        # Check if ghost is dead
        if ghost_hp <= 0:
            break

        # Ghost attacks back (only happens on a low roll)
        ghost_roll = random.randint(1, 6)
        if ghost_roll <= 2:
            player_hp = player_hp - 1
            print("  The shadow strikes back! Your health: " + str(player_hp))

        print()

        # Check if player died
        if player_hp <= 0:
            print("\n  The darkness consumes you.")
            print("  You feel yourself fading... becoming one with the campground.")
            print("  You are now part of the curse.\n")
            log_event("CHALLENGE_ATTEMPT", "FAIL", "Encounter=ShadowEncounter PlayerDied Rounds=" + str(combat_round))
            state["player_health"] = 0
            state["challenge_shadow_result"] = "fail"
            state["ending"] = "become_part_of_curse"
            return state

    # Ghost was defeated
    print("\n  The shadow lets out a wail and dissolves into mist!")
    print("  The path to the ritual site is open!\n")

    log_event("CHALLENGE_ATTEMPT", "SUCCESS", "Encounter=ShadowEncounter Rounds=" + str(combat_round))

    # Save updated player health back to state
    state["player_health"] = player_hp
    state["challenge_shadow_result"] = "success"

    return state
