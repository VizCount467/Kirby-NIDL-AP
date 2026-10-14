# Kirby Nightmare in Dream Land Archipelago

Welcome to the Kirby Nightmare in Dreamland Archiepelago implementation. This game is fully playable, and development is ongoing with various planned features. The client is stable and the game is functional, but some undetected bugs may still exist. Please report any bugs/issues to [the AP Discord thread](https://discord.com/channels/731205301247803413/1533318615057567885) in "future-game-design". 

## General Structure

All levels and doors are unlocked from the start, except for boss doors. You will not be able to enter the boss door until obtaining the required number of Star Rod Pieces. Collect all necessary Star Rod pieces and defeat Nightmare at the Fountain of Dreams to win. See [the guide in the docs](https://github.com/VizCount467/Kirby-NIDL-AP/blob/master/kirbynidl/docs/en_Kirby_Nightmare_in_Dream_Land.md) for more detailed game information and info on the configurable options. 

## Installation

Download the kirbynidl.apworld file from the latest GitHub release and install it by opening it the Archipelago program or moving it into your "custom worlds" folder. From there, it should work the same as any other custom GBA AP game. 

See the [setup file in the docs](https://github.com/VizCount467/Kirby-NIDL-AP/blob/master/kirbynidl/docs/setup_en.md) for complete details.
Also check out the [Poptracker by Blakel](https://github.com/blakelmenakle/KNiDL-Poptracker), if interested. 

## Features Currently Implemented
- Locations
    - All level clears
    - All world bosses
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
    - Death Link!

## Features Planned To be Implemented
- Option to access Worlds early if that world's warp star station is unlocked (Warp Station Access Early)

## Speculative Features

- Locations
    - Win minigames in specific worlds
- Items
    - Unlock individual levels (complicates ability logic)
- Kirby Palette changer (implemented in other randomizers of the game)
- Level and/or World Shuffle (not sure where to even begin) (also complicates ability logic)
- Enemy Ability Shuffle (complicates ability logic)
- Option to play as Meta Knight (Kirby still plays the final boss? Stop at Dedede?)
- Energy Link Support
- On-Screen AP Text (via either the nightmare defeated story narration or the label that appears at the top of the screen in each overworld lobby) (maybe the credits too??)

## Known Bugs and Issues

- The game may crash at the GBA BIOS. Set Bizhawk to skip the BIOS if this is a problem for you.
- Getting grabbed by certain midbosses with invincibility active may still hurt Kirby (and can make the invincibility theme play until the next room)
- The interaction of savestates and the various client-dependent game interactions is completely unknown -- use save states at your own risk!

## Latest Updates (See Releases for Full Changelog)

- 10/7/26: 
    - Added Death Link!
    - Added Overworld door color manipulation to indicate completion (flashing red if a level has unchecked locations, yellow for full clear)
    - Items have their vanilla effects when collected a second time after a reset, to help with replaying levels. 
    - Added the "Kirby actionable" IWRAM flag to client and ASM actions (will help prevent crashes, probably)
    - Fixed the starting vitality option not working and defaulting to 3
- 10/8/26:
    - Fixed bug in hijacked healing routine where the Kirby "actionable" flag wasn't being reset
- 10/14/26:
    - Added client "starrod" and "abilities" command
    - Updated docs with BIOS crash note, poptracker links
    - Fixed client not receiving starting inventory
    - Added Warp Station skips to Options, Tests, and gen logic (no client yet though)


## Credits and Shout-Outs

- Thanks to the RetroAchievements community for getting me started with their RAM map documentation
- Thanks to aquova and their [KNDL-Rando Repo](https://github.com/Aquova/KNDL-Rando) for additional RAM mapping and initial draft of an ability-locking system. 
- Thanks to fellow GBA APWorld devs brodieberger ([Mega Man Zero 3](https://github.com/brodieberger/MMZero3Archipelago)) and lilDavid ([Wario Land 4](https://github.com/lilDavid/Archipelago-Wario-Land-4)). Many structures and concepts from their code were studied and utilized in this project. 