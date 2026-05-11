# security/security.py
# CyberScape: The Cursed Campground
# Cyber Role: Dom DeLeat
# This file handles two things:
#   1. Audit logging  - writing important game events to a text file
#   2. Input validation - making sure the player types valid input

import datetime

# The name of the log file we write to
AUDIT_LOG_FILE = "audit_log.txt"


# --------------------------------------------------
# AUDIT LOGGING
# --------------------------------------------------

def get_timestamp():
    # Returns the current date and time as a readable string
    # Example output: "2026-05-09 14:35:21"
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def log_event(event_type, result="", details=""):
    # Writes one line to audit_log.txt describing something that happened
    # event_type = what kind of event  (example: "GAME_START")
    # result     = "SUCCESS" or "FAIL" or leave blank for neutral events
    # details    = any extra info you want to include

    # Build the log line piece by piece
    line = get_timestamp() + " - " + event_type

    # Only add result and details if they were provided
    if result != "":
        line = line + " - " + result
    if details != "":
        line = line + " - " + details

    # Write the line to the log file
    # "a" means append - we add to the end instead of erasing the file
    try:
        log_file = open(AUDIT_LOG_FILE, "a")
        log_file.write(line + "\n")
        log_file.close()
    except:
        # If we can't write to the file, just print a warning
        # We do NOT crash the game over a logging error
        print("[WARNING] Could not write to audit log.")


# --------------------------------------------------
# INPUT VALIDATION
# --------------------------------------------------

def get_int_choice(prompt, low, high, scene=""):
    # Keeps asking the player for a number until they type a valid one
    # prompt = the question shown to the player
    # low    = the lowest allowed number
    # high   = the highest allowed number
    # scene  = the current scene name (used in the log, optional)
    #
    # Example: get_int_choice("Pick 1-3: ", 1, 3)
    # This will not crash if the player types "abc" or "99"

    while True:
        player_input = input(prompt)

        # Try to convert what the player typed into a whole number
        try:
            choice = int(player_input)

            # Check if the number is within the allowed range
            if choice >= low and choice <= high:
                return choice  # Valid! Return the number.
            else:
                # Number was valid but out of range
                log_event("INPUT_INVALID", "FAIL", "Scene=" + scene + " Input=" + player_input + " OutOfRange")
                print("  Invalid choice. Please enter a number from " + str(low) + " to " + str(high) + ".")

        except ValueError:
            # int() failed because the player typed letters or symbols
            log_event("INPUT_INVALID", "FAIL", "Scene=" + scene + " Input=" + player_input + " NotANumber")
            print("  Please enter a number from " + str(low) + " to " + str(high) + ".")


def get_text_input(prompt):
    # Keeps asking the player for text until they type something (not blank)
    # Returns the player's answer as a string

    while True:
        player_input = input(prompt)

        # Remove extra spaces from the start and end
        player_input = player_input.strip()

        if player_input != "":
            return player_input  # Got something, return it
        else:
            print("  Input cannot be empty. Please try again.")


def confirm_action(prompt):
    # Asks the player a yes/no question
    # Returns True if they said yes, False if they said no

    while True:
        player_input = input(prompt + " (y/n): ")
        player_input = player_input.strip().lower()  # lowercase so Y and y both work

        if player_input == "y" or player_input == "yes":
            return True
        elif player_input == "n" or player_input == "no":
            return False
        else:
            print("  Please enter 'y' for yes or 'n' for no.")
