# engine/state.py
# Role 1 - Rachel Philip
# Responsibility: Game state management.
# All game state lives in one dictionary called `state`.
# This module creates that dictionary and provides helper
# functions for reading and updating it safely.
#
# Every other module receives `state` as a parameter and
# reads/writes it through these helpers — nothing reaches
# into the dict directly except through the functions below.

# =====================
# STATE CREATION
# =====================

def new_state():
    """
    Create and return a fresh game state for a new game.

    The state dictionary is the single source of truth for
    everything that has happened in the current playthrough.

    Keys:
        inventory (list) : Item names the player is currently holding.
        flags     (dict) : Boolean story flags set by NPC interactions
                           and player choices. Used to track what the
                           player knows and what they have done.
        npc_met   (set)  : Names of NPCs already encountered.
                           Prevents the same NPC intro from replaying.
        path      (str)  : Which of the 3 story paths the player chose.
                           Set in scene_opening. Values: 'investigate',
                           'escape', 'help', or '' before chosen.
        ending    (str)  : Which ending the player reached.
                           Set just before the ending scene runs.
                           Values: 'break', 'escape', 'become', or None.

    Returns:
        dict : A default starting game state.
    """
    return {
        "inventory": [],
        "flags":     {},
        "npc_met":   set(),
        "path":      "",
        "ending":    None,
    }
create_new_state = new_state
game_is_over = lambda state: state.get("curse_broken") or state.get("escaped") or state.get("cursed") or state.get("player_health", 5) <= 0
print_state_summary = lambda state: print(state)
# =====================
# FLAG HELPERS
# =====================

def set_flag(state, flag_name):
    """
    Set a story flag to True.

    Flags are used to track story progress — for example,
    whether the player has spoken to a certain NPC or found
    a key clue. They are checked later to control story branches.

    Parameters:
        state     (dict) : The current game state.
        flag_name (str)  : The name of the flag to set.

    Example:
        set_flag(state, "ranger_lore")
        # Later in story.py:
        if get_flag(state, "ranger_lore"):
            print("The ranger already told you about the curse.")
    """
    state["flags"][flag_name] = True


def get_flag(state, flag_name):
    """
    Check whether a story flag has been set.

    Returns False safely if the flag was never set,
    so callers never get a KeyError.

    Parameters:
        state     (dict) : The current game state.
        flag_name (str)  : The flag name to check.

    Returns:
        bool : True if the flag was set, False otherwise.
    """
    return state["flags"].get(flag_name, False)


# =====================
# NPC TRACKING HELPERS
# =====================

def mark_npc_met(state, npc_name):
    """
    Record that the player has met a specific NPC.

    Parameters:
        state    (dict) : The current game state.
        npc_name (str)  : A short key for the NPC, e.g. 'old_ranger'.
    """
    state["npc_met"].add(npc_name)


def has_met_npc(state, npc_name):
    """
    Check whether the player has already met a specific NPC.

    Used by scene functions to skip the intro dialogue on
    repeat visits to the same location.

    Parameters:
        state    (dict) : The current game state.
        npc_name (str)  : The NPC key to check.

    Returns:
        bool : True if the player has already met this NPC.
    """
    return npc_name in state["npc_met"]


# =====================
# PATH + ENDING HELPERS
# =====================

def set_path(state, path_name):
    """
    Record which story path the player has chosen.

    Called in scene_opening when the player makes their
    first major decision.

    Parameters:
        state     (dict) : The current game state.
        path_name (str)  : 'investigate', 'escape', or 'help'.
    """
    state["path"] = path_name


def set_ending(state, ending_name):
    """
    Set the ending that will play when the game concludes.

    Called by the ghost challenge or the early escape scene
    once the outcome is determined.

    Parameters:
        state       (dict) : The current game state.
        ending_name (str)  : 'break', 'escape', or 'become'.
    """
    state["ending"] = ending_name
