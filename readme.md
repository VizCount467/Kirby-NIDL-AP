# Kirby Nightmare in Dream Land Archipelago

Welcome to the Kirby Nightmare in Dreamland Archiepelago implementation by me, VizCount. This is currently a work in progress and is not close to being a fully functional apworld. Feel free to watch my progress in updates to this readme file, or contact me on the Archieplago Discord sever.

## General Structure

All levels and doors are unlocked from the start, except for boss doors. You will not be able to enter the boss door until obtaining the requisite number of Star Rod Pieces. ie, you must collect 1 star rod piece to fight the World 1 boss, 2 for the World 2 boss, et. Collect all 7 Star Rod pieces and defeat Nightmare at the Fountain of Dreams to win. 

## Installation

Place the kirbynidl folder in your Archipelago worlds directory and run AP from source. You may also need to place a US Kirby Nightmare in Dreamland ROM in your main Archipelago directory with the correct file name. As in, I'm not sure I've figured out automatic ROM file selection through system dialogue. Other than this, I can't guarantee any other setup will work yet. 

## Features Currently Implemented
- Locations
    - Clearing a Level (World 1 Only)
    - Consumable item pickups (Pep Drinks, Maxim Tomatoes, and 1ups) (World 1 Only)
- Items
    - Consumable Pickups (Pep Drinks, 1ups, Maxim Tomatoes, Invincibility Candy)
    - "Star Rod Pece" (unlocks world Boss and next world)

## Features Planned To be Implemented
- Locations
    - All level clears
    - All world boss clears
    - All consumable items (besides Candy)
    - All Big Switches
- Items
    - Unlock Copy Abilities
    - Unlock minigames and other side doors (Museum, Arena, Warp Star Station, et)
    - Vitality Upgrades

## Speculative Features

- Locations
    - Win minigames in specific worlds

- Items
    - Unlock individual levels

- Kirby Palette changer (implemented in other randomizers of the game)
- Level and/or World Shuffle (not sure where to even begin)

## Known Bugs and Issues

- As a side effect of unlocking all levels, overworld door sprites are not loaded until the boss is defeated
- All awarded healing items heal for one point only (working on this!)
- The life counter displays incorrectly (ie, 28) after receiving a life from AP, but this self-corrects after loading a new room
- It may be possible to enter a "locked" overworld door by using fast copy abilities (burning, wheel, hi-jump) - need to test this



