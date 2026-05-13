# CyberScape: The Cursed Campground

A text-based adventure game built in Python with a cybersecurity twist!

## Team Members

| Name | Role |
|------|------|
| Doug | Core Engine + Integration |
| Racheal | Core Engine + Integration |
| Riya| Story + Gameplay Systems |
| Milo | Story + Gameplay Systems |
| Dom Deloatch | Challenges + Cybersecurity |
| Dom Deloatch | Challenges + Cybersecurity |

---

## How to Run the Game

**Requirements:** Python 3.10 or higher

1. Clone the repository:
   ```
   git clone https://github.com/domdelo/cyse130-group3-project.git
   cd cyse130-group3-project
   ```

2. Run the game:
   ```
   python/python3 main.py
   ```

3. Follow the on-screen prompts to play. Type a number and press Enter to make choices.

**Note:** A save file (`savegame.json`) and audit log (`audit_log.txt`) will be created in the same folder when you play.

---

## Core Game Features

- 3 branching story paths leading to 3 different endings
- 5 unique locations and major events
- 5 NPCs with dialogue and meaningful interactions
- Inventory system with 5 collectible items
- 2 challenges (puzzle + combat)
- Full Cyber Pack: input validation, audit logging, and save/load tamper detection

---

## Story Paths and Endings

### Story Paths

**Path 1 — Investigate the Legend**
The player chooses to dig into the history of the campground. They search the old ranger station, decode a hidden message, and uncover the origin of the curse. This path leads toward breaking the curse permanently.

**Path 2 — Try to Escape Immediately**
The player ignores the mystery and tries to find a way out of the campground. They encounter the ghostly figure blocking the exit road and must fight or outwit it to flee. This path leads to escaping — but the curse continues.

**Path 3 — Help a Lost Camper**
The player hears a child crying in the woods and goes to help. The lost camper leads them deeper into the cursed circle. This path can end in the player becoming part of the curse if they are not prepared.

### Endings

**Ending 1 — Break the Curse**
The player completes the ritual at the cursed circle using the items collected along the way. The campground is freed. All missing campers reappear. The player walks out at sunrise.

**Ending 2 — Escape but Curse Continues**
The player escapes through the forest road but leaves the curse behind. As they drive away they see the campground lights flicker back on in the rearview mirror.

**Ending 3 — Become Part of the Curse**
The player is overwhelmed by the shadow encounter or makes too many wrong choices. The darkness claims them. They become the next ghostly figure, doomed to wander the campground.

---

## Locations and Major Events

| # | Location / Event | Description |
|---|-----------------|-------------|
| 1 | Camp Entrance | The player arrives at the empty campground and must decide their first move |
| 2 | Ranger Station | An abandoned station with a locked supply shed — contains the cipher puzzle |
| 3 | The Dark Woods | A branching forest path where the lost camper is found and strange sounds occur |
| 4 | The Cursed Circle | A clearing deep in the woods where the shadow encounter takes place |
| 5 | The Ritual Site | The source of the curse — final location where the player can attempt to break it |

---

## NPCs

| NPC | Location | Role |
|-----|----------|------|
| Old Ranger (Ranger Holt) | Ranger Station (via note) | Leaves behind a coded message (cipher clue) and the only map of the campground |
| Lost Kid | The Dark Woods | Leads the player deeper into the woods; triggers Path 3 |
| Ghostly Figure | The Cursed Circle | Main obstacle — blocks the path to the ritual site; triggers the Shadow Encounter challenge |
| Suspicious Camper | Camp Entrance | Gives the player a warning and optionally trades items; changes available inventory |
| Journal Owner | Ranger Station / Ritual Site | Communicates through journal entries scattered across locations; reveals the curse's origin and how to break it |

---

## Inventory Items

| Item | Where to Get It | Purpose |
|------|----------------|---------|
| Flashlight | Camp Entrance (starting item) | Required to explore the Dark Woods at night without a penalty |
| Master Key | Ranger Station shed (cipher puzzle reward) | Unlocks the gate to the Ritual Site |
| Holy Water | Suspicious Camper (trade) | Gives +3 damage bonus in the Shadow Encounter combat |
| Silver Compass | Dark Woods (found on ground) | Gives +2 damage bonus in Shadow Encounter; also points toward the Ritual Site |
| Ranger's Torch | Ranger Station shed | Gives +1 damage bonus in Shadow Encounter; lights the Cursed Circle to reveal hidden symbols |

---

## Challenges

### Challenge 1 — The Ranger's Cipher
**Location:** Ranger Station

**What the player must do:**
Decode a Caesar cipher found in a note left by Ranger Holt. Each letter in the coded word must be shifted back by 3 in the alphabet to find the password. The coded word is `I L U H Z R R G` and the answer is `FIREWOOD`. The player has 3 attempts.

**Success:** The supply shed unlocks. The player receives the Master Key and a journal page with coordinates to the Cursed Circle.

**Failure:** The player uses all 3 attempts without getting the right answer. A loud alarm sound triggers, setting a flag that makes the Shadow Encounter harder in a later scene.

---

### Challenge 2 — The Shadow Encounter
**Location:** The Cursed Circle

**What the player must do:**
A ghostly figure blocks the path to the Ritual Site. The player chooses one of three strategies: Fight (direct combat using dice rolls), Distract (throw an object and hope for a lucky roll of 4+), or Flee (give up the encounter and go back). In combat, the player deals 1 base damage per round plus bonuses from items in their inventory (Holy Water +3, Silver Compass +2, Ranger's Torch +1). The ghost has 3 HP.

**Success:** The ghost is defeated or successfully distracted. The path to the Ritual Site opens and the player can attempt to break the curse.

**Failure:** The player's health reaches 0 during combat or they flee. If health hits 0, the game ends with the "Become Part of the Curse" ending. If they flee, they are forced back to the campsite and must find another way.

---

## Cyber Pack

### 1. Input Validation and Safe Error Handling
**File:** `security/security.py`

All player input in the game goes through two helper functions: `get_int_choice()` and `get_text_input()`. `get_int_choice()` uses a `try/except` block to catch `ValueError` when the player types letters instead of a number, and also checks that the number is within the allowed range. If either check fails, the player is shown an error message and re-prompted — the game never crashes. `get_text_input()` prevents blank entries from being accepted. Every invalid input is also written to the audit log.

### 2. Audit Logging
**File:** `security/security.py` — function: `log_event()`

Every important game event is written as a timestamped line to `audit_log.txt`. Events logged include: game start and end, invalid input attempts, story choices made, challenge attempts (with success/fail and number of attempts), items used, and save/load attempts. Each line follows this format:
```
2026-05-09 14:35:21 - EVENT_TYPE - RESULT - details
```
Example lines:
```
2026-05-09 14:35:21 - GAME_START - Player started a new game
2026-05-09 14:36:02 - INPUT_INVALID - FAIL - Scene=main_menu Input=abc NotANumber
2026-05-09 14:37:10 - CHALLENGE_ATTEMPT - SUCCESS - Puzzle=RangersCipher Attempts=2
2026-05-09 14:38:05 - SAVE_ATTEMPT - SUCCESS - File=savegame.json
2026-05-09 14:38:31 - LOAD_ATTEMPT - FAIL - Reason=SAVE_TAMPERED
```

### 3. Save and Load with Tamper Detection
**File:** `security/save_load.py`

When the player saves, the game state is written to `savegame.json` as JSON. Before saving, a SHA-256 hash of the entire game state is computed using Python's `hashlib` library and stored inside the save file under the key `__integrity_hash__`. When the player loads, the hash is recomputed from the current file contents and compared to the stored hash. If someone manually edits the save file (for example, setting player health to 999), the hash will not match and the load is rejected with a warning message. The save is deleted and a new game starts automatically.
