# Kirby Nightmare in Dream Land Archipelago

Welcome to the in-progress Kirby Nightmare in Dream Land Archipelago implementation project (developer VizCount). This document should contain all the necessary information to understand the alterations to the game, the options, and where development currently is.


## General Information

The goal of Kirby Nightmare in Dream Land is to collect all pieces of the Star Rod and defeat Nightmare at the end of the Fountain of Dreams. By default, all levels are unlocked, but pieces of the Star Rod are required to enter Boss levels. For example, you must obtain 2 pieces of the Star Rod before fighting Paint Roller in World 2. You must have all 7 to enter the Fountain of Dreams and win. Specifically, game clear status is granted upon viewing the end-of-game cutscene/narration following the moon explosion.  

Clearing every normal level, boss, and Arena challenge will grant a check, as well as every Big Switch. By default, every food item (Pep Drink and Maxim Tomato) and 1up in normal levels is also a check. Maxim tomatos and 1ups given in other minigames besides Arenas are NOT checks. 

Kirby cannot obtain any copy abilities until that copy ability is unlocked via Archipelago. Kirby also begins with a reduced number of max health segments, with more unlockable via AP items. Kirby may also receive Pep Drink, Maxim Tomatos, 1ups, and invincibility Candy at any time in a level via the AP client. Kirby can only receive these items once per save file (a counter is saved in the file data) (WIP). 

All items, inlcuding client-side unblockers (door keys, unlocked abilities, Star Rod pieces) will play a specific sound effect when received based on their item type. However, you must watch the AP tracker feed to know what specific item was received, as well as what items were sent via location checks. 

## Options (NOT YET IMPLEMENTED/SPECULATIVE)

- `Number of Star Rod Pieces`:
    Set the number of Star Rod Pieces in the item pool (minimum 7)

- `Number of Required Star Rod Pieces`
    Set the raw number of Star Rod Pieces to unlock the World 7 boss door and complete the game.
    The requirement for every other world's boss door will be this number divided by 7, rounded down.
    If the number resulting from the "Percent" option is lower and still meets the minimum 7 requirement, that number will overwrite this option

- `Percent of Required Star Rod Pieces`
    Set the percent of Star Rod Pieces in the item pool required to unlock the World 7 boss door and complete the game
    The requirement for every other world's boss door will be the resulting number divided by 7, rounded down.
    If the "Raw Number" option is lower than the resulting number from this option and still meets the minimum 7 requirement, that number will overwrite this option


- `Lock Bonus Doors`:
    Locks all doors to minigames and other side areas (Arenas, Museums, Warp Star Stations) until the correponding key is obtained. Adds Bonus door keys to the item pool

- `Lock Copy Abilities`:
    If switched to False, unlocks all copy abilities from the start of the game

- `Randomize Pickups`:
    If switched to False, food items and 1ups are no longer checks. May not be compatible with item-heavy settings, i.e. keys. 

- `Starting Vitality`:
    Number of health segments Kirby starts the game with. Can be any number from 1-6.

- `Maximum Vitality`:
    Number of health segments Kirby can possibly obtain. Can be any number of 1-6. A number of vitality items equal to this minus the starting vitality will be added to the item pool. 

