# Mega Man Zero 3 Archipelago

Welcome to the in-progress Kirby Nightmare in Dream Land Archipelago implementation project (developer VizCount). This document should contain all the necessary information to understand the alterations to the game, the options, and where development currently is.


## General Information

As in the original, the aim of the game and sole victory condition is to collect all pieces of the Star Rod and defeat Nightmare at the end of the Fountain of Dreams. By default, all levels are unlocked, but borrowing the structure from the Core Kirby's Dream Land 3 implementation (roughly), pieces of the Star Rod are required to enter Boss levels. For example, you must obtain 2 pieces of the Star Rod before fighting Paint Roller in World 2. You must have all 7 to enter the Fountain of Dreams and win. 

Clearing every normal level and boss will grant a check, as well as every Big Switch. By default, every food item (Pep Drink and Maxim Tomato) and 1up in normal levels is also a check. Maxim tomatos and 1ups given in the Arena and other minigames are NOT checks. 

Kirby cannot obtain any copy abilities until that copy ability is unlocked via AP (except for the Meta Knight Sword, that one's free for logistic reasons). Kirby also begins with a reduced number of max health segments, with more unlockable via AP items. Kirby may also receive Pep Drink, Maxim Tomatos, 1ups, and invincibility Candy at any time in a level via AP. Kirby can only receive these items once per save file (a counter is saved in the file data). 

Non-tangible items (door keys, ublocked abilities, Star Rod pieces) will play a specific sound effect when received. However, you must watch the AP tracker feed to know what was received (as well as what items were sent via checks). 

## Options

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

