from dataclasses import dataclass
from Options import Choice, Range, Toggle, OptionSet, PerGameCommonOptions

##Not to be implemented until much later, if ever, because it would hugely complicate ability access logic
# class LockLevelDoors(Toggle):
#     """Locks all doors to normal levels in the overworld until a Key item is collected. Adds level keys to the item pool."""
#     display_name = "Lock Normal Level Doors"

class NumberStarRod(Range):
    """Number of Star Rod Pieces in the item pool"""
    display_name = "Number of Star Rod Pieces"
    range_start = 7
    range_end = 56
    default = 7

class ReqNumStarRod(Range):
    """Number of Star Rod Pieces required to beat the game"""
    display_name = "Required Number of Star Rod Pieces"
    range_start = 7
    range_end = 56
    default = 7

class ReqPrcStarRod(Range):
    """Percent of Star Rod Pieces required to beat the game. Set to 0 to use Required Number instead"""
    display_name = "Required Percent of Star Rod Pieces"
    range_start = 0
    range_end = 100
    default = 0

class AdvancedLogic(Toggle):
    """Incorporates various difficult, obscure, or unintuitive tricks into item placement logic. Check game page for more info"""
    display_name = 'Advanced Logic'

class LockBonusDoors(Toggle):
    """Locks all doors to minigames, arenas, museums and warp star stations in the overworld until a Key Item is collected. Adds bonus door keys to the item pool"""
    display_name = "Lock Bonus Doors"

class LockCopyAbilities(Toggle):
    """Prevents Kirby from using copy abilities until unlocked. Adds copy ability unlocks to the item pool"""
    display_name = "Lock Copy Abilities"

## Postponing this as an option, since it would require changing the ROM patch procedure to leave the heling item routine alone
# class RandomizePickups(Toggle):
#     """Adds all Pep Drinks, Maxim Tomatoes, and 1ups in normal levels to the location pool"""
#     display_name = "Randomize Pickups"

class StartingVitality(Range):
    """Number of health segments Kirby will start the game with"""
    display_name = "Starting Vitality"
    range_start = 1
    range_end = 6
    default = 3

class MaxVitality(Range):
    """Maximum number of health segments Kirby can obtain after obtaining all vitality items. A number of vitality items equal to this minus the starting vitality will be added to the item pool"""
    display_name = "Maximum Vitality"
    range_start = 1
    range_end = 6
    default = 6

@dataclass
class KirbyNIDLOptions(PerGameCommonOptions):
    num_pieces: NumberStarRod
    req_pieces_num: ReqNumStarRod
    req_pieces_prc: ReqPrcStarRod
    advanced_logic: AdvancedLogic
    lock_bonus_doors: LockBonusDoors
    lock_copy_abilities: LockCopyAbilities
    #randomize_pickups: RandomizePickups
    starting_vitality: StartingVitality
    max_vitality: MaxVitality