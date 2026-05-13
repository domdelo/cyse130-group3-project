# content/story.py
# CyberScape: The Cursed Campground
# Student: Story scenes and branching logic

from security.security import log_event

# -------------------------
# SCENES (STRUCTURED)
# -------------------------
scenes = {

    "start": {
        "text": "You arrive at a quiet campground. The sun is setting. A sign reads: 'WARNING: Stay after dark at your own risk.'",
        "choices": [
            {"desc": "Investigate the legend", "next": "legend_path"},
            {"desc": "Try to escape immediately", "next": "escape_path"},
            {"desc": "Help a lost camper", "next": "help_path"}
        ]
    },

    # -------------------------
    # PATH 1: LEGEND
    # -------------------------
    "legend_path": {
        "text": "You decide to investigate the disappearances. You find an old ranger near a fire.",
        "choices": [
            {"desc": "Talk to the ranger", "next": "ranger_scene"},
            {"desc": "Explore abandoned cabin", "next": "cabin_scene"}
        ]
    },

    "ranger_scene": {
        "text": "The ranger warns you: 'The curse feeds on fear. Find the journal.'",
        "effect": lambda state: state["flags"].update({"met_ranger": True}),
        "choices": [
            {"desc": "Search for the journal", "next": "journal_scene"}
        ]
    },

    "cabin_scene": {
        "text": "Inside the cabin, you hear whispers. Something watches you.",
        "effect": lambda state: state["flags"].update({"visited_cabin": True}),
        "choices": [
            {"desc": "Stay and investigate", "next": "ghost_scene"},
            {"desc": "Run outside", "next": "legend_path"}
        ]
    },

    "journal_scene": {
        "text": "You find a dusty journal explaining how to break the curse.",
        "effect": lambda state: state["flags"].update({"has_journal": True}),
        "choices": [
            {"desc": "Perform the ritual", "next": "good_ending"},
            {"desc": "Ignore it", "next": "bad_ending"}
        ]
    },

    # -------------------------
    # PATH 2: ESCAPE
    # -------------------------
    "escape_path": {
        "text": "You try to leave, but the roads seem different. The forest shifts.",
        "choices": [
            {"desc": "Keep driving", "next": "loop_scene"},
            {"desc": "Turn back", "next": "start"}
        ]
    },

    "loop_scene": {
        "text": "You keep driving in circles. The same sign appears again.",
        "choices": [
            {"desc": "Panic and run into woods", "next": "ghost_scene"},
            {"desc": "Accept fate", "next": "neutral_ending"}
        ]
    },

    # -------------------------
    # PATH 3: HELP CAMPER
    # -------------------------
    "help_path": {
        "text": "You find a lost kid crying near the trees.",
        "choices": [
            {"desc": "Help the kid", "next": "kid_scene"},
            {"desc": "Ignore and leave", "next": "escape_path"}
        ]
    },

    "kid_scene": {
        "text": "The kid thanks you and gives you a strange charm.",
        "effect": lambda state: state["flags"].update({"helped_kid": True}),
        "choices": [
            {"desc": "Follow the kid", "next": "ghost_scene"}
        ]
    },

    # -------------------------
    # SHARED EVENT
    # -------------------------
    "ghost_scene": {
        "text": "A ghostly figure appears. It whispers your name.",
        "effect": lambda state: state["flags"].update({"saw_ghost": True}),
        "choices": [
            {"desc": "Confront it", "next": "challenge_scene"},
            {"desc": "Run", "next": "escape_path"}
        ]
    },

    # -------------------------
    # CHALLENGE EVENT (Puzzle/Decision)
    # -------------------------
    "challenge_scene": {
        "text": "The ghost asks: 'Do you understand the curse?'",
        "choices": [
            {
                "desc": "Yes (requires journal)",
                "next": "good_ending",
                "condition": lambda state: state["flags"].get("has_journal", False)
            },
            {
                "desc": "No",
                "next": "bad_ending"
            }
        ]
    },

    # -------------------------
    # ENDINGS
    # -------------------------
    "good_ending": {
        "text": "You perform the ritual correctly. The curse is broken. The campground is silent.",
        "effect": lambda state: state.update({"curse_broken": True}),
        "end": True
    },

    "neutral_ending": {
        "text": "You escape... but the curse remains for others.",
        "effect": lambda state: state.update({"escaped": True}),
        "end": True
    },

    "bad_ending": {
        "text": "You feel cold. You are now part of the curse.",
        "effect": lambda state: state.update({"cursed": True}),
        "end": True
    }
}


# -------------------------
# HELPER FUNCTION
# -------------------------
def get_available_choices(scene, state):
    # Filter choices based on conditions
    # Returns only choices the player is currently allowed to pick
    valid_choices = []

    for choice in scene.get("choices", []):
        if "condition" not in choice or choice["condition"](state):
            valid_choices.append(choice)

    return valid_choices
