# Kirby Nightmare in Dream Land Archipelago

Welcome to the Kirby Nightmare in Dreamland Archiepelago implementation by me, VizCount. This is currently a work in progress and is not close to being a fully functional apworld. Feel free to watch my progress in updates to this readme file, or contact me on the Archieplago Discord sever.

## General Structure

All levels and doors are unlocked from the start, except for boss doors. You will not be able to enter the boss door until obtaining the requisite number of Star Rod Pieces. ie, you must collect 1 star rod piece to fight the World 1 boss, 2 for the World 2 boss. Collect all 7 Star Rod pieces and defeat Nightmare at the Fountain of Dreams to win. 

## Installation

Place the kirbynidl folder in your Archipelago worlds directory and run AP from source. Youl will also need to place a US Kirby Nightmare in Dreamland ROM in your main Archipelago directory with the correct file name if not prompted by the patch sequence. Other than Source, I can't guarantee any other setup will work yet. 

## Features Currently Implemented
- Locations
    - Clearing a Level (World 1 Only)
    - Consumable item pickups (Pep Drinks, Maxim Tomatoes, and 1ups) (World 1 Only)
    - Defeating a Boss (World 1 Only)
- Items
    - Consumable Pickups (Pep Drinks, 1ups, Maxim Tomatoes, Invincibility Candy)
        - Health items are not awarded immediately, but added to a "Bank". HP is automatically restored from the bank as you take damage.
        - Consumable items are single-use. If you quit and re-open the same save file on the same saved game, you will not receive items received during the last session(the HP bank also resets)
    - "Star Rod Piece" (unlocks world Boss and next world)
    - Unlock Copy Abilities (currently Sword Only)
    - Vitality (Max HP Upgrades) (currently only 1)

## Features Planned To be Implemented
- Locations
    - All level clears
    - All world boss clears
    - All consumable items (Pep Drinks, 1ups, Maxim Tomatoes)
    - All Big Switches
- Items
    - The final victory Condition
    - Unlock minigames and other side doors (Museum, Arena, Warp Star Station, et)

## Speculative Features

- Locations
    - Win minigames in specific worlds

- Items
    - Unlock individual levels

- Kirby Palette changer (implemented in other randomizers of the game)
- Level and/or World Shuffle (not sure where to even begin)
- Enemy Ability Shuffle

## Known Bugs and Issues

- As a side effect of unlocking all levels, overworld door sprites are not loaded until the boss is defeated
- The life counter displays incorrectly (ie, 28) after receiving a life from AP, but this self-corrects after loading a new room
- The life counter may be calculated incorrectly sometimes after client awards 1ups? Need more testing here 
- It may be possible to enter a "locked" overworld door by using fast copy abilities (wheel, hi-jump) - need to test this
- When Kirby tries to open a "locked" door, the intended SFX plays EVERY FRAME (will resolve soon)
- The Item Sync Counter may not be stored in saveRAM as intended, leading to all received items being awarded on startup. 
- Invinciblity Candy will trigger location checks because it uses the "Feed Me" function. The client needs to be designed with awareness of these non-locations
- When Kirby swallows a copy ability that's not unlocked yet, the "ability get" SFX and Kirby pose may still play out, even though no ability is awarded (minor)
- The interaction of the client-dependent ability locking with the mix roulette is still unknown -- may need to nullify mixes entirely
- The interaction of savestates and the various client-dependent game interactions is completely unknown (minor?)

## Latest Updates

- 8/3/26: Added "HP Bank" feature modeled off the Mega Man 2/3 AP that stores HP items if you don't immediately them, and gives HP 1 segment as a time as you take damage
- 8/5/26: Added Detection for boss defeat via the Kirby Dance BGM. Attempted to add SFX for the Star Rod piece.
- 8/10/26: Added Vitality and Copy Ability unlocks (currently 1 vitality, and just Sword). Fixed SFX for all awarded items


