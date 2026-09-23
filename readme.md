# Kirby Nightmare in Dream Land Archipelago

Welcome to the Kirby Nightmare in Dreamland Archiepelago implementation by VizCount. This game is currently PLAYABLE, but not yet finalized for release -- consider it in an "alpha" state. Development is ongoing, and any updates are summarized at the bottom of this readme file, as well as currently known bugs/issues.  

## General Structure

All levels and doors are unlocked from the start, except for boss doors. You will not be able to enter the boss door until obtaining the requisite number of Star Rod Pieces. Collect all necessary Star Rod pieces and defeat Nightmare at the Fountain of Dreams to win. See the guide in the "docs" folder for more detailed game information and configurable options. 

## Installation

Download the kirbynidl.apworld file from the latest GitHub release and install it by opening it the Archipelago program or moving it into your "custom worlds" folder. Create or Join a game to get a .apknidl patch file. Open this patch file with the AP program, and select your US Kirby Nightmare in Dream Land ROM file if prompted. From there, Bizhawk should open automatically if your settings are configured properly. However, you must manually enter the Server and Port information in the client when it starts up. 

See the setup file in the docs for complete details.

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
- Option to use open Warp Star stations to skip bosses (slightly complicates logic, requires ASM tinkering)
- Option to play as Meta Knight (Kirby still plays the final boss? Stop at Dedede?)
- Energy Link Support
- On-Screen AP Text (via either the nightmare defeated story narration or the label that appears at the top of the screen in each overworld lobby) (maybe the credits too??)

## Known Bugs and Issues

- Warp Star stations may not open upon beating the boss, and not all unlocked worlds may be acessible. Resetting the game should fix this
- If you are disconnected from the server and beat a boss, that location check will be permanently LOST since bosses cannot be refought on the same file
- Getting grabbed by certain midbosses with invincibility active may still hurt Kirby (and can make the invincibility theme play until the next room)
- The interaction of savestates and the various client-dependent game interactions is completely unknown -- use save states at your own risk!

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
- 9/13/26: Add Tests. Fix logic bug with Star Rod progression
- 9/15/26: Polishing and bug squashing. Fixes attempted for following bugs:
    - Overworld door locking does not lock doors in levels (re: 4-6 stake room, 6-2 rocky room)
    - Item awarding no longer attempted in Nightmare Orb phase (healing is impossible) 
    - Big Switch state partly moved game side to ensure Overworld is always open. Client sets "all switches pressed" while game always reads "no switches pressed" in Big Switch rooms. 
    - Fixed 5-1 location ID's
    - Expanded 5-5 Big Switch Logic. 
- 9/17/26: Further Polishing. Update Docs with implementation details. Added All essential Tests and tightened Rules.py logic. Fixes Attempted for following bugs
    - Add missing Pep Drink in 4-3 to locations
    - Client "sync counter" goes to length of items received if internal counter somehow greater than network instead of resetting
- 9/18/26: Polishing. Add Vitality Count Tests. Attempted following bug fixes
    - 6-6 UFO's trigger the "level clear" check due to detection oversights
    - Location checks now allow multiple ID's to be sent in one tick of the client instead of assuming only 1 (checks would be eaten)
    - Healing should NOT be attempted in the Nightmare Orb phase (again)
    - Healing SHOULD be allowed in Arenas
    - Healing should NOT be attempted in the event of a pit death (HP = 0)
- 9/19/26: Bug testing. Attempted following bug fixes
    - Warp Star stations are all initially barred, then have all 7 worlds unlocked upon reset
    - Useless healing attempts in the intro to the Nightmare Wizard fight (getting there!)
- 9/21/26: Final Bug Testing. Following Fixes applied
    - Warp Star stations will not have all 7 worlds unlocked to start, even after a reset
    - Added missing spike room 1up in 3-3
    - Fixed Arena Key logic and added Arena Key test
- 9/22/26: Final-er Bug Testing. Preparations for release
    - Update docs to prep for release
    - Enable automatic patching from patch file and prompt for initial ROM file selection
    - Fix implementation of copy abilities and side doors initially unlocked options
    - Fix Arena checks being awarded immediately at the start of the fight

