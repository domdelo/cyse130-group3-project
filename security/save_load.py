# security/save_load.py
# CyberScape: The Cursed Campground
# Cyber Role: Dom DeLeat
# This file handles saving and loading the game.
# It also checks if someone cheated by editing the save file manually.
# How the tamper check works:
#   - When we save, we scramble all the game data into a short code (a SHA-256 hash)
#   - We store that code inside the save file
#   - When we load, we re-scramble the data and compare codes
#   - If the codes don't match, someone edited the file and we reject it

import json
import hashlib
import os

from security.security import log_event

# The file we save to
SAVE_FILE = "savegame.json"

# This is the key name we use inside the save file to store the hash code
# We picked a weird name so it's obvious it's not regular game data
HASH_KEY = "__integrity_hash__"


# --------------------------------------------------
# HELPER: COMPUTE THE HASH
# --------------------------------------------------

def compute_hash(game_data):
    # Takes the game data dictionary and turns it into a short unique code (hash)
    # If even one character in the data changes, the hash will be totally different
    # That's how we detect cheating / tampering

    # First, build a copy of the data WITHOUT the stored hash inside it
    # (We don't want to hash the hash itself - that would be circular)
    data_to_hash = {}
    for key in game_data:
        if key != HASH_KEY:
            data_to_hash[key] = game_data[key]

    # Convert the dictionary to a JSON string with keys in alphabetical order
    # sort_keys=True is important - same data must always produce same string
    data_string = json.dumps(data_to_hash, sort_keys=True)

    # Run SHA-256 on the string to get the hash code
    # encode() converts the string to bytes, which hashlib needs
    hash_code = hashlib.sha256(data_string.encode()).hexdigest()

    return hash_code


# --------------------------------------------------
# SAVE GAME
# --------------------------------------------------

def save_game(state):
    # Saves the game state dictionary to savegame.json
    # Also computes and stores a hash so we can detect tampering later
    # Returns True if the save worked, False if something went wrong

    try:
        # Make a copy of the state so we don't change the original
        save_data = {}
        for key in state:
            save_data[key] = state[key]

        # Compute the hash and add it to the save data
        save_data[HASH_KEY] = compute_hash(save_data)

        # Write everything to the save file
        # indent=2 makes the file readable if you open it in a text editor
        save_file = open(SAVE_FILE, "w")
        json.dump(save_data, save_file, indent=2)
        save_file.close()

        log_event("SAVE_ATTEMPT", "SUCCESS", "File=" + SAVE_FILE)
        print("  [SAVE] Game saved successfully!")
        return True

    except:
        log_event("SAVE_ATTEMPT", "FAIL", "Could not write save file")
        print("  [SAVE] ERROR: Could not save the game.")
        return False


# --------------------------------------------------
# LOAD GAME
# --------------------------------------------------

def load_game():
    # Loads game state from savegame.json
    # Checks the hash to make sure the file was not tampered with
    # Returns the game state dictionary if everything is good
    # Returns None if the file is missing, broken, or tampered

    # Check if the save file even exists
    if not os.path.exists(SAVE_FILE):
        log_event("LOAD_ATTEMPT", "FAIL", "Reason=FILE_NOT_FOUND")
        print("  [LOAD] No save file found. Starting a new game.")
        return None

    # Try to read and parse the JSON file
    try:
        save_file = open(SAVE_FILE, "r")
        raw_data = json.load(save_file)
        save_file.close()
    except:
        log_event("LOAD_ATTEMPT", "FAIL", "Reason=FILE_CORRUPTED")
        print("  [LOAD] Save file is corrupted and cannot be read.")
        return None

    # Check that the hash key is actually in the file
    if HASH_KEY not in raw_data:
        log_event("LOAD_ATTEMPT", "FAIL", "Reason=HASH_MISSING")
        print("  [LOAD] Save file is missing its security data. Cannot load.")
        return None

    # Pull out the hash that was stored when we saved
    stored_hash = raw_data[HASH_KEY]

    # Recompute the hash from the current file contents
    expected_hash = compute_hash(raw_data)

    # Compare the two hashes
    if stored_hash != expected_hash:
        # They don't match - the file was edited after saving
        log_event("LOAD_ATTEMPT", "FAIL", "Reason=SAVE_TAMPERED")
        print("  [LOAD] WARNING: Your save file has been tampered with!")
        print("  [LOAD] The security check failed. Starting a new game.")
        return None

    # Hashes match - the file is clean
    # Build the game state without the internal hash key
    log_event("LOAD_ATTEMPT", "SUCCESS", "File=" + SAVE_FILE)
    print("  [LOAD] Save verified. Welcome back to the campground...")

    game_state = {}
    for key in raw_data:
        if key != HASH_KEY:
            game_state[key] = raw_data[key]

    return game_state


# --------------------------------------------------
# DELETE SAVE
# --------------------------------------------------

def delete_save():
    # Deletes the save file (used when starting fresh after a tampered save)
    # Returns True if deleted successfully or file didn't exist

    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            log_event("SAVE_DELETE", "SUCCESS", "File=" + SAVE_FILE)
            return True
        except:
            log_event("SAVE_DELETE", "FAIL", "Could not delete save file")
            return False

    return True  # File didn't exist, nothing to delete
