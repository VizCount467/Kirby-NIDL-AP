from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#boilerplate to ensure no namespace errors when we define the World in function spec. Forces type annotations to not be evaluated immediately
#actually importing it would probably be a circular import and also would be slow

from BaseClasses import ItemClassification, Location
from . import items

# Every location must have a unique integer ID associated with it (no need to be sequential)
# Common practice seems to be to pick a unique base number and offset from there
# For my Kirby NIDL, Let's use 3 digits, first for world, second for level, third sequential
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
    "Vegetable Valley - Boss (Whispy Woods)" : 150
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


