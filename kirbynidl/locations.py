from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#boilerplate to ensure no namespace errors when we define the World in function spec. Forces type annotations to not be evaluated immediately
#actually importing it would probably be a circular import and also would be slow

from BaseClasses import ItemClassification, Location
from . import items

#Every location must have a unique integer ID associated with it (no need to be sequential)
#Common practice seems to be to pick a unique base number and offset from there
#For my Kirby NIDL, Let's use 3 digits, first for world, second for level, third sequential
#The level clear will always be XX0, and items in the level XX(+n)
#The Big Switch will always be XX9 (works because there are never more than 8 items in a single level) (3-6 comes close though!)
#Boss level checks will always be X99 for convenient calculation, even if technically the boss level is just the next sequential level (ie, level 5 in W1)
#The world's Arena will be X89
#Something similar can be done for Minigame checks, if those ever happen
LOCATION_TABLE_READABLE = {
    "Vegetable Valley 1 - Level Clear" : 110,
    "Vegetable Valley 1 - Tomato (Waterfall)" : 111,

    "Vegetable Valley 2 - Level Clear" : 120,
    "Vegetable Valley 2 - Tomato (Cave)" : 121,
    "Vegetable Valley 2 - 1up (Hidden Room)" : 122,

    "Vegetable Valley 3 - Level Clear" : 130,
    "Vegetable Valley 3 - Tomato (Hotheads)" : 131,

    "Vegetable Valley 4 - Level Clear" : 140,
    "Vegetable Valley 4 - Pep Drink (Platform)" : 141,
    "Vegetable Valley 4 - 1up (Shotzos)" : 142,
    "Vegetable Valley 4 - Candy (Stump)" : 143,

    "Vegetable Valley - Boss (Whispy Woods)" : 199,


    "Ice Cream Island 1 - Level Clear" : 210,
    "Ice Cream Island 1 - Pep Drink (Cave)" : 211,

    "Ice Cream Island 2 - Level Clear" : 220,
    "Ice Cream Island 2 - Pep Drink (Wheelie Road)": 221,
    "Ice Cream Island 2 - Pep Drink (Before Goal)" : 222,
    "Ice Cream Island 2 - 1up (Under Goal)" : 223,

    "Ice Cream Island 3 - Level Clear" : 230,
    "Ice Cream Island 3 - Tomato (UFO Room)" : 233,
    "Ice Cream Island 3 - 1up (Cave Tunnel)" : 231,
    "Ice Cream Island 3 - Pep Drink (Underwater)" : 232,

    "Ice Cream Island 4 - Level Clear" : 240,
    "Ice Cream Island 4 - 1up (Gip Room)" : 242,
    "Ice Cream Island 4 - Tomato (Block cage)" : 241,
    "Ice Cream Island 4 - Pep Drink (Laser Room 1)" : 244, 
    "Ice Cream Island 4 - Pep Drink (Laser Room 2)" : 246,
    "Ice Cream Island 4 - Pep Drink (Laser Room 3)" : 245,
    "Ice Cream Island 4 - 1up (Laser Room 4)" : 243,
    "Ice Cream Island 4 - Pep Drink (Sand Detour)" : 247,

    "Ice Cream Island 5 - Level Clear" : 250,
    "Ice Cream Island 5 - Pep Drink (Forest Far Right)" : 251,
    "Ice Cream Island 5 - Pep Drink (Gordo Pond)" : 257, 
    "Ice Cream Island 5 - 1up (Metal Blocks 1)" : 252,
    "Ice Cream Island 5 - 1up (Metal Blocks 2)" : 253,
    "Ice Cream Island 5 - 1up (Gordo Guarded)" : 254,
    "Ice Cream Island 5 - Pep Drink (Starman Room)" : 255,
    "Ice Cream Island 5 - Tomato (Poppy Bros. Jr.)" : 256,

    "Ice Cream Island - Boss (Paint Roller)" : 299,


    "Butter Building 1 - Level Clear" : 310,
    "Butter Building 1 - Pep Drink (Big Switch Room)" : 311,

    "Butter Building 2 - Level Clear" : 320,
    "Butter Building 2 - Tomato (Poppy Bros. Jr.)" : 321,
    "Butter Building 2 - Pep Drink (Fire Escape)" : 322,
    "Butter Building 2 - Tomato (Before Bugsy Left)" : 324,
    "Butter Building 2 - 1up (Before Bugsy Right" : 323,

    "Butter Building 3 - Level Clear" : 330,
    "Butter Building 3 - Tomato (Parallel Rooms)" : 331,

    "Butter Building 4 - Level Clear" : 340,
    "Butter Building 4 - 1up (Updraft Room 1)" : 342,
    "Butter Building 4 - Tomato (Updraft Room 2)" : 341,
    "Butter Building 4 - Pep Drink (Updraft Room 3)" : 343,

    "Butter Building 5 - Level Clear" : 350,
    "Butter Building 5 - Candy (First Room)" : 351,
    "Butter Building 5 - Pep Drink (Fire Escape)" : 352,
    "Butter Building 5 - Tomato (After Bonkers 1)" : 353,
    "Butter Building 5 - 1up (After Bonkers 2)" : 354,

    "Butter Building 6 - Level Clear" : 360,
    "Butter Building 6 - Pep Drink (Laser Room)" : 361,
    "Butter Building 6 - Tomato (Ladder Room)" : 362,
    "Butter Building 6 - Pep Drink (Defog Room)" : 363,
    "Butter Building 6 - Pep Drink (Before Big Switch)" : 368,
    "Butter Building 6 - 1up (Dark Room)" : 364,
    "Butter Building 6 - Pep Drink (Hi Jump Room Mid Right)" : 367,
    "Butter Building 6 - Tomato (Hi Jump Room End Left)" : 365,
    "Butter Building 6 - 1up (Hi Jump Room End Right)" : 366,

    "Butter Building - Boss (Mr. Shine and Mr. Bright)" : 399,


    "Grape Garden 1 - Level Clear" : 410,

    "Grape Garden 2 - Level Clear" : 420,
    "Grape Garden 2 - Tomato (Sqishy Room)" : 422,
    "Grape Garden 2 - Pep Drink (Spiky Hallway)" : 422,

    "Grape Garden 3 - Level Clear" : 430,
    "Grape Garden 3 - 1up (Cannon)" : 432,
    "Grape Garden 3 - Tomato (Blimp Interior)" : 431,

    "Grape Garden 4 - Level Clear" : 440,
    "Grape Garden 4 - 1up (Wheel Race)" : 441,

    "Grape Garden 5 - Level Clear" : 450,
    "Grape Garden 5 - Candy (first Room)" : 451,
    "Grape Garden 5 - Tomato (Sqishy Room)" : 452,
    "Grape Garden 5 - Pep Drink (Hidden Room)" : 453,
    "Grape Garden 5 - 1up (Hidden Room Underside)" : 457,
    "Grape Garden 5 - 1up (Burning Room Bottom)" : 454,
    "Grape Garden 5 - 1up (Burning Room Top)" : 455,
    "Grape Garden 5 - Pep Drink (Burning Room Middle)" : 456,

    "Grape Garden 6 - Level Clear" : 460,
    "Grape Garden 6 - Pep Drink (Poolside)" : 461,
    "Grape Garden 6 - 1up (Stake)" : 462,
    "Grape Garden 6 - Pep Drink (Near Goal)" : 463,

    "Grape Garden - Boss (Kracko)" : 499,


    "Yogurt Yard 1 - Level Clear" : 510,
    "Yogurt Yard 1 - 1up (Rocky Room)" : 512,
    "Yogurt Yard 1 - Pep Drink (Skydive Room)" : 511,
    "Yogurt Yard 1 - Pep Drink (Big Switch Room)" : 514,

    "Yogurt Yard 2 - Level Clear" : 520,
    "Yogurt Yard 2 - 1up (Before Bonkers)" : 521,
    "Yogurt Yard 2 - 1up (Under the Mountain)" : 522,

    "Yogurt Yard 3 - Level Clear" : 530,
    "Yogurt Yard 3 - Tomato (Stake Room Left)" : 533,
    "Yogurt Yard 3 - 1up (Stake Room Right)" : 532,
    "Yogurt Yard 3 - Pep Drink (Spike Descent)" : 531,

    "Yogurt Yard 4 - Level Clear" : 540,
    "Yogurt Yard 4 - 1up (Spike Tunnel)" : 541,
    "Yogurt Yard 4 - Tomato (Before Big Switch 1)" : 544,
    "Yogurt Yard 4 - 1up (Before Big Switch 2)" : 543,
    "Yogurt Yard 4 - Pep Drink (Big Waterfall Cave)" : 542,

    "Yogurt Yard 5 - Level Clear" : 550,
    "Yogurt Yard 5 - Tomato (Forest Thicket)" : 551,

    "Yogurt Yard 6 - Level Clear" : 560,
    "Yogurt Yard 6 - Tomato (Wheelie Room)" : 561,
    "Yogurt Yard 6 - Tomato (Big Switch Room Right)" : 563,
    "Yogurt Yard 6 - 1up (Big Switch Room Left)" : 562,

    "Yogurt Yard - Boss (Heavy Mole)" : 599,


    "Orange Ocean 1 - Level Clear" : 610,
    "Orange Ocean 1 - 1up (Metal Blocks)" : 611,
    "Orange Ocean 1 - Tomato (Before Big Switch Left)" : 613,
    "Orange Ocean 1 - 1up (Before Big Switch Right)" : 612,

    "Orange Ocean 2 - Level Clear" : 620,
    "Orange Ocean 2 - Pep Drink (Bomb Block)" : 621,
    "Orange Ocean 2 - 1up (Rocky Room)" : 624,
    "Orange Ocean 2 - Tomato (Poppy Bros. Jr.)" : 622,

    "Orange Ocean 3 - Level Clear" : 630,
    "Orange Ocean 3 - Pep Drink (Ladder)" : 631,
    "Orange Ocean 3 - Pep Drink (Bonkers Room)" : 632,
    "Orange Ocean 3 - 1up (Man Overboard!)" : 636,
    "Orange Ocean 3 - Tomato (Laser Ball Room)" : 637,
    "Orange Ocean 3 - Pep Drink (After Bonkers)" : 633,
    "Orange Ocean 3 - 1up (Right Window Secret)" : 635,
    "Orange Ocean 3 - 1up (Left Window Secret)" : 634,

    "Orange Ocean 4 - Level Clear" : 640,
    "Orange Ocean 4 - Pep Drink (Flooded Alcove)" : 646,
    "Orange Ocean 4 - 1up (Beam Bomb Block 1)" : 642,
    "Orange Ocean 4 - 1up (Beam Bomb Block 2)" : 643,
    "Orange Ocean 4 - 1up (Beam Bomb Block 3)" : 644,
    "Orange Ocean 4 - 1up (Cave Detour)" : 641,
    "Orange Ocean 4 - Pep Drink (Below Bomber)" : 645,

    "Orange Ocean 5 - Level Clear" : 650,
    "Orange Ocean 5 - Tomato (Cliff Top)" : 651,
    "Orange Ocean 5 - 1up (Cannon Pit)" : 652,

    "Orange Ocean 6 - Level Clear" : 660,
    #Technically, the ID's here are 9, 10 and 11 because of the UFO's. The client will have a carve-out for this special case
    "Orange Ocean 6 - Tomato (UFO Room)" : 661, 
    "Orange Ocean 6 - Candy (After Poppy Bros. Sr.)" : 663,
    "Orange Ocean 6 - 1up (Upper Path Metal Blocks)" : 662,

    "Orange Ocean - Boss (Meta Knight)" : 699,


    "Rainbow Resort 1 - Level Clear" : 710,
    "Rainbow Resort 1 - 1up (Laser Room)" : 711,
    "Rainbow Resort 2 - Pep Drink (Block Tunnel)" : 661,

    "Rainbow Resort 2 - Level Clear" : 720,
    "Rainbow Resort 2 - 1up (Hard Midboss Reward 1)" : 723,
    "Rainbow Resort 2 - 1up (Hard Midboss Reward 2)" : 724,
    "Rainbow Resort 2 - 1up (Hard Midboss Reward 3)" : 725,
    "Rainbow Resort 2 - 1up (Hard Midboss Reward 4)" : 722,
    "Rainbow Resort 2 - 1up (Hard Midboss Reward 5)" : 726,
    "Rainbow Resort 2 - Tomato (Near Goal)" : 711,

    "Rainbow Resort 3 - Level Clear" : 730,
    "Rainbow Resort 3 - Tomato (Icy Climb)" : 731,
    "Rainbow Resort 3 - Candy (Icy Path)" : 732,
    "Rainbow Resort 3 - 1up (Slope Shotzo)" : 733,
    "Rainbow Resort 3 - Pep Drink (Shotzo Gauntlet 1)" : 734,
    "Rainbow Resort 3 - Pep Drink (Shotzo Gauntlet 2)" : 735,
    "Rainbow Resort 3 - Tomato (Shotzo Gauntlet 3)" : 736,
    "Rainbow Resort 3 - 1up (Shotzo Gauntlet 4)" : 737,

    "Rainbow Resort 4 - Level Clear" : 740,
    "Rainbow Resort 4 - 1up (Behind Gordo)" : 741,

    "Rainbow Resort 5 - Level Clear" : 750,
    "Rainbow Resort 5 - Pep Drink (Cannon Room)" : 751,
    "Rainbow Resort 5 - 1up (Cannon Reward 1)" : 756,
    "Rainbow Resort 5 - 1up (Cannon Reward 2)" : 754,
    "Rainbow Resort 5 - 1up (Cannon Reward 3)" : 755,
    "Rainbow Resort 5 - 1up (Cannon Reward 4)" : 753,
    "Rainbow Resort 5 - 1up (Cannon Reward 5)" : 752,

    "Rainbow Resort 6 - Level Clear" : 760,
    "Rainbow Resort 6 - Tomato (Castle Lololo 1)" : 761,
    "Rainbow Resort 6 - 1up (Castle Lololo 2)" : 762,
    "Rainbow Resort 6 - Pep Drink (Float Islands 1)" : 764,
    "Rainbow Resort 6 - Tomato (Float Islands 2)" : 763,
    "Rainbow Resort 6 - Tomato (Moon Room 1)" : 766,
    "Rainbow Resort 6 - 1up (Moon Room 2)" : 765,
}

KNIDL_BASE_ID = 2742740
LOCATION_NAME_TO_ID = {
    k:LOCATION_TABLE_READABLE[k]+KNIDL_BASE_ID for k in LOCATION_TABLE_READABLE.keys()
}

# Helper function stolen from APQuest. Returns a subset of the big LOCATION ID dictionary to feed to the region.add_location function
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

# Each Location instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Location class and override the "game" field.
class KirbyNIDLLocation(Location):
    game = "Kirby Nightmare in Dream Land"

#function to be called once regions have been added to the World
#locations are added to the World by adding them to their regions
#you can also make a location via the constructor, but since every must have a region, this makes more sense
def create_all_locations(world: KirbyNIDLWorld) -> None:

    #TODO: list out all the regions once we have the full list built instead of hardcoding here. Greater abstraction will come!
    for region_name in ["Vegetable Valley 1","Vegetable Valley 2","Vegetable Valley 3","Vegetable Valley 4","Vegetable Valley"]:
        r = world.get_region(region_name)
        #Grab all location id mappings that start with the region name for levels
        if region_name[-1].isdigit():
            r_locs = get_location_names_with_ids(k for k in LOCATION_NAME_TO_ID.keys() if k.startswith(region_name))
            r.add_locations(r_locs,KirbyNIDLLocation)
        #Put the boss locations in the main World
        else:
            r_locs = get_location_names_with_ids(k for k in LOCATION_NAME_TO_ID.keys() if k.startswith(region_name) and '- Boss' in k)
            r.add_locations(r_locs,KirbyNIDLLocation)

    #If we want to add an event ("fake" location used in game logic but not actually a check), do this also
    #Here, we create a "Victory" event to make declaring World completion easier
    #In this 1-world iteration of NIDL, we'll just put this event on Whispy Woods being defeated (change the name eventually to "Nightmare defeated, et")
    #Note, this "final boss defeated" event is created in this statement, and can be accessed like a location
    #the "Victory" is also created in this statement, and is accessed like an item in logical requirements
    r = world.get_region('Vegetable Valley')
    r.add_event(
            "Final Boss Defeated", "Victory", location_type=KirbyNIDLLocation, item_type=items.KirbyNIDLItem
        )


