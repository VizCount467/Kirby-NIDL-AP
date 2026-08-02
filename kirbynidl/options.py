from dataclasses import dataclass
from Options import Choice, Range, Toggle, OptionSet, PerGameCommonOptions

##Not to be implemented until much later, if ever, because it would hugely complicate ability access logic
# class LockLevelDoors(Toggle):
#     """Locks all doors to normal levels in the overworld until a Key item is collected. Adds level keys to the item pool."""
#     display_name = "Lock Normal Level Doors"

class LockBonusDoors(Toggle):
    """Locks all doors to minigames, arenas, museums and warp star stations in the overworld until a Key Item is collected. Adds bonus door keys to the item pool"""
    display_name = "Lock Bonus Doors"

class LockCopyAbilities(Toggle):
    """Prevents Kirby from using copy abilities until unlocked. Adds copy ability unlocks to the item pool"""
    display_name = "Lock Copy Abilities"

class RandomizePickups(Toggle):
    """Adds all Pep Drinks, Tomatos, and 1ups in normal levels to the location pool"""
    display_name = "Randomize Pickups"

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
    # lock_level_doors: LockLevelDoors
    lock_bonus_doors: LockBonusDoors
    lock_copy_abilities: LockCopyAbilities
    randomize_pickups: RandomizePickups
    starting_vitality: StartingVitality
    max_vitality: MaxVitality