# Kirby Nightmare in Dream Land Archipelago

Welcome to the in-progress Kirby Nightmare in Dream Land Archipelago implementation project (developer VizCount). This document should contain all the necessary information to understand how to play, the alterations made to the base game, and how to use the options.


## General Information

The goal of Kirby Nightmare in Dream Land is to collect all pieces of the Star Rod and defeat Nightmare at the end of the Fountain of Dreams. By default, all levels are unlocked, but pieces of the Star Rod are required to enter Boss levels. For example, you must obtain 2 pieces of the Star Rod before fighting the World 2 Boss. You must have all 7 pieces to enter the Fountain of Dreams and win. Specifically, game clear status is granted upon viewing the moon explosion cutscene following defeat of the final boss.  

Clearing every normal level, boss, and Arena challenge will grant a check, as well as every Big Switch. Every food item and 1up in normal levels is also a check. Maxim tomatoes given in arenas are not checks (only clearing the Arena itself is), and 1ups given out in minigames are NOT checks. 

Kirby cannot obtain any copy abilities until that copy ability is unlocked via Archipelago. Kirby also begins with a reduced number of max health segments, with more unlockable via AP items. Kirby may also receive Pep Drink, Maxim Tomatoes, 1ups, and invincibility Candy at any time in a level via the AP client.

All items, inlcuding client-side unblockers (door keys, unlocked abilities, Star Rod pieces) will play a specific sound effect when received based on their item type. However, you must watch the AP tracker feed to know what specific item was received, as well as what items were sent via location checks. 

Kirby Nightmare in Dreamland automatically saves your progress after every level and boss clear. Big Switches will always appear in levels, even if their location has already been checked. Consumable items will also reappear, but not in the same play session. If you quit and begin a new session, the consumable items awarded in previous sessions will NOT be awarded again. As in, the items awarded by the client DO sync between sessions by use of in-game save RAM. 

Make sure to connect to the client before exiting the title screen / file menu. I canot guarantee anything in this mod is compatible with the vanilla multiplayer features. Finally, use savestates as your own risk!


## Options (NOT YET IMPLEMENTED)

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

- `Randomize Pickups`:
    If switched to False, food items and 1ups are no longer checks. However, they may still be awarded as filler items. May not be compatible with some settings. 

- `Starting Vitality`:
    Number of health segments Kirby starts the game with. Can be any number from 1-6.

- `Maximum Vitality`:
    Number of health segments Kirby can possibly obtain. Can be any number of 1-6. A number of vitality items equal to this minus the starting vitality will be added to the item pool. 

