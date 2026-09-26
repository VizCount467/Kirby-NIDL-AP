# Kirby Nightmare in Dream Land Archipelago

Welcome to the Kirby Nightmare in Dreamland Archiepelago implementation. This game is currently PLAYABLE and in an EARLY RELEASE phase. The client is stable and the game is functional, but some undetected bugs may still exist. Please report any bugs/issues to [the AP Discord thread](https://discord.com/channels/731205301247803413/1533318615057567885) in "future-game-design". 

## General Structure

All levels and doors are unlocked from the start, except for boss doors. You will not be able to enter the boss door until obtaining the required number of Star Rod Pieces. Collect all necessary Star Rod pieces and defeat Nightmare at the Fountain of Dreams to win. See [the guide in the docs](https://github.com/VizCount467/Kirby-NIDL-AP/blob/master/kirbynidl/docs/en_Kirby_Nightmare_in_Dream_Land)for more detailed game information and info on the configurable options. 

## Installation

Download the kirbynidl.apworld file from the latest GitHub release and install it by opening it the Archipelago program or moving it into your "custom worlds" folder. From there, it should work the same as any other custom GBA AP game. 

See the [setup file in the docs](https://github.com/VizCount467/Kirby-NIDL-AP/blob/master/kirbynidl/docs/setup_en.md) for complete details.

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
    - Star Rod Piece - unlocks world Boss and next world
    - Unlock Copy Abilities 
    - Unlock Minigames (Bomb Rally, Air Grind, Quick Draw) and other side doors (Arena, Museum, Warp Station) for each world
        - NOTE: Doors that are NOT locked behind big switches in the vanilla game, ie the World 1 Museum, start as locked. All possible doors are shuffled in!
    - Vitality (Max HP Upgrades) - currently fixed at 3 upgrades with 3 Max HP to start, configurable in the options
        - Vitality pieces also affect the amount of HP you get from consumables. 
            - Pep Drinks give 1 HP at 3 Max HP or lower, 2 HP otherwise
            - Maxim Tomatos give N-1 HP, where N is the Max HP
- Options
    - Variable number of existing and required Star Rod Pieces
    - Variable starting health and number of health upgrades
    - Start with all Copy Abilities and/or bonus doors unlocked, if desired
    - Toggle obscure/difficult tricks in location logic

## Features Planned To be Implemented
- Death link Support

## Speculative Features

- Locations
    - Win minigames in specific worlds
- Items
    - Unlock individual levels (complicates ability logic)
- Kirby Palette changer (implemented in other randomizers of the game)
- Level and/or World Shuffle (not sure where to even begin) (also complicates ability logic)
- Enemy Ability Shuffle (complicates ability logic)
- Option to use open Warp Star stations to skip bosses (slightly complicates logic, requires ASM tinkering)
- Option to play as Meta Knight (Kirby still plays the final boss? Stop at Dedede?)
- Energy Link Support
- On-Screen AP Text (via either the nightmare defeated story narration or the label that appears at the top of the screen in each overworld lobby) (maybe the credits too??)

## Known Bugs and Issues

- Getting grabbed by certain midbosses with invincibility active may still hurt Kirby (and can make the invincibility theme play until the next room)
- The interaction of savestates and the various client-dependent game interactions is completely unknown -- use save states at your own risk!

## Latest Updates (See Releases for Full Changelog)

- 9/25/26: Fixed bugs found in previous release. Removed "beta" and "unstable" language.
    - Warp Star stations are no longer always boarded up before restart, and have the appropriate destinations unlocked for currently unlocked worlds
    - Added failsafe for missing boss checks -- on initialization, the client checks in-game values and awards all cleared boss locations, if necessary.
    - Fixed door lock bug in ASM allowing "locked" OW doors to be entered
    - Clean up 7-1 Big Switch Rules
    - Rename various locations to give them more personality


## Credits and Shout-Outs

- Thanks to the RetroAchievements community for getting me started with their RAM map documentation
- Thanks to aquova and their [KNDL-Rando Repo](https://github.com/Aquova/KNDL-Rando) for additional RAM mapping and initial draft of an ability-locking system. 
