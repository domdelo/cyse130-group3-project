from systems.inventory import add_item

def ranger_npc(state):
    print("[RANGER] \nRanger: 'The forest is dangerous at night. Here, take this lantern")
    add_item(state, "lantern")
    state["met_ranger"] = True

def kid_npc(state):
    print("[KID] \nKid: 'I found this strange charm. You can have it.'")
    add_item(state, "charm")
    state["helped_kid"] = True

def scientist_npc(state):
    print("[SCIENTIST] \nScientist: 'I've been studying this forest for years. My journal will tell you how to break the curse. '")
    add_item(state, "has_journal")

def guard_npc(state):
    print("[GUARD] \nGuard: 'You need the lantern to pass.'")
    if "lantern" in state.get("inventory", []):
        print("[GUARD] \nGuard: 'Ah, you have the lantern. You may pass.'")
        state["met_guard"] = True
    else: 
        print("[GUARD] \nGuard: 'You don't have the lantern. You cannot pass.'")

def ghost_npc(state):
    print("[GHOST] \nGhost: 'You shouldn't have come. Now, answer my question or remain trapped here forever'")
    state["met_ghost"] = True
