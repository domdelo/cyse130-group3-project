#INVENTORY
#stores player items to be used in the game

#adds an item to the player's inventory
def add_item(state, item):
    if "inventory" not in state: #initialize and create inventory list if it doesn't exist
        state["inventory"] = []
    state["inventory"].append(item) 
    print(f"[INVENTORY] Added {item} to inventory.")


#removes existing item from the player's inventory
def remove_item(state, item):
    if "inventory" in state and item in state["inventory"]:
        state["inventory"].remove(item)
        print(f"[INVENTORY] Removed {item} from inventory.")
    else:
        print(f"[INVENTORY] Cannot remove {item}. It is not in inventory.")

#checks if item already exists in the player's inventory
def has_item(state, item):
    return item in state.get("inventory", []) #will return True/False

#allows player to view their complete inventory
def view_inventory(state):
    inventory = state.get("inventory", [])
    print("\n==========================")
    print(f"[INVENTORY] Total items: {len(inventory)}")
    if inventory:
        print("[INVENTORY] You have the following items:")
        for item in inventory:
            print(f" - {item}")
    else:
        print("[INVENTORY] Your inventory is empty.")
    print("==========================\n")