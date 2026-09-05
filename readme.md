# Kirby Nightmare in Dream Land Archipelago

Welcome to the Kirby Nightmare in Dreamland Archiepelago implementation by VizCount. This game is currently PLAYABLE, but not yet finalized for release -- consider it in an "alpha" state. Development is ongoing, and any updates are summarized at the bottom of this readme file, as well as currently known bugs/issues.  

## General Structure

All levels and doors are unlocked from the start, except for boss doors. You will not be able to enter the boss door until obtaining the requisite number of Star Rod Pieces. ie, you must collect 1 star rod piece to fight the World 1 boss, 2 for the World 2 boss. Collect all 7 Star Rod pieces and defeat Nightmare at the Fountain of Dreams to win. See the guide in the "docs" folder for more detailed game information. 

## Installation

Place the kirbynidl folder in your Archipelago worlds directory and run Archipelago from source. You will also need to place a US Kirby Nightmare in Dreamland ROM in your main Archipelago directory with the correct file name if not prompted by the patch sequence. Other than Source, I can't guarantee any other setup will work yet. Check the "setup_en" file in the "docs" folder for an alternative instllation summary. 

## Features Currently Implemented
- Locations
    - All level clears
    - All world boss clears
    - All in-level consumable items (Pep Drinks, 1ups, Candy, Maxim Tomatoes)
    - All Big Switches
    - All Arenas
- Items
    - Consumable Pickups (Pep Drinks, 1ups, Maxim Tomatoes, Invincibility Candy)
        - Health items are not awarded immediately, but added to a "Bank". HP is automatically restored from the bank as you take damage.
        - Consumable items are single-use. If you quit and re-open the same save file on the same saved game, you will not receive items received during the last session (the HP bank also resets)
    - "Star Rod Piece" (unlocks world Boss and next world)
    - Unlock Copy Abilities 
    - Unlock Minigames (Bomb Rally, Air Grind, Quick Draw) and other side doors (Arena, Museum, Warp Station) for each world
        - NOTE: Doors that are NOT locked behind big switches in the vanilla game, ie the World 1 Museum, start as locked. All possible doors are shuffled in!
    - Vitality (Max HP Upgrades) - currently fixed at 3 upgrades with 3 Max HP to start
        - Vitality pieces also affect the amount of HP you get from consumables. 
            - Pep Drinks give 1 HP at 3 Max HP or lower, 2 HP otherwise
            - Maxim Tomatos give N-1 HP, where N is the Max HP

## Features Planned To be Implemented
- Death link Support

## Speculative Features

- Locations
    - Win minigames in specific worlds
- Items
    - Unlock individual levels (complicates ability logic)
- Kirby Palette changer (implemented in other randomizers of the game)
- Level and/or World Shuffle (not sure where to even begin) (also complicates ability logic)
- Enemy Ability Shuffle (immensely complicates ability logic)
- Option to play as Meta Knight (Kirby steps in at final boss? Stop at Dedede?)
- Energy Link Support
- On-Screen AP Text (via either the nightmare defeated story narration or the label that appears at the top of the screen in each overworld lobby) (maybe the credits too??)

## Known Bugs and Issues

- As a side effect of unlocking all levels, overworld door sprites are not loaded until the boss is defeated and the game is reloaded
- The Healing / HP Bank system may not work in the final battle
- Generation may be unoptimized. Gen with this in big games at your own risk!
- The interaction of savestates and the various client-dependent game interactions is completely unknown (minor - use save states at your own risk!)
- Sometimes, the state of the overworld may have none of the big switches pressed. Try entering/exiting a level or other overworld lobbies, and this should fix itself (?)

## Latest Updates

- 8/3/26: Added "HP Bank" feature modeled off the Mega Man 1/2/3 AP that stores HP items if you don't immediately them, and gives HP 1 segment as a time as you take damage
- 8/5/26: Added Detection for boss defeat via the Kirby Dance BGM. Attempted to add SFX for the Star Rod piece.
- 8/10/26: Added Vitality and Copy Ability unlocks (currently 1 vitality, and just Sword). Fixed SFX for all awarded items
- 8/13/26: Added (untested) big switch detection logic. Attempted to fix EVERY FRAME door SFX issue. Added (soon to be useless) coordinate logic for in-level pickups
- 8/14/26: Overhauled item detection to use collection flags in RAM rather than coordinates. Added (untested) Arena clear detection
- 8/20/26: Add full-game locations, items and logic rules
- 8/26/26: Overhaul Door locking system to go in-game instead of client side. Debug Big Switch Checks
- 8/28/26: Fix client sync counter bug. Update guide in apworld docs. Other misc bug-squashing.
- 9/3/26: Overhaul Ability locking system to go in-game, fixing issues concerning copy abilities and the mix roulette. Fixed door lock edge case
- 9/4/26: Add functional options to client and world


