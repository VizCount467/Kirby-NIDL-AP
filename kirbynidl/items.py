from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations.py for explanation of this boilerplate

from BaseClasses import Item, ItemClassification

# Every item must have a unique integer ID associated with it.
# We will have a lookup from item name to ID here that, in world.py, we will import and bind to the world class.
# Even if an item doesn't exist on specific options, it must be present in this lookup.
# Common practice is to offset these ID's to an arbitrary base id to prevent collisions, like in locations

ITEM_TABLE_READABLE = {
    ##LEVEL KEYS: not in use, would complicate ability acessibility logic immensely
    ##LEVEL KEYS: Format 1WL
    # 'Vegetable Valley 1 Level Key' : 111,
    # 'Vegetable Valley 2 Level Key' : 112,
    # 'Vegetable Valley 3 Level Key' : 113,
    # 'Vegetable Valley 4 Level Key' : 114,
    ##Abilities: Format 2XX, where XX is ID in client script
    ##Misc
    'Star Rod Piece' : 1,
    ##Filler pickup items: Format 1X, where X is ID in client script
    'Pep Drink' : 11,
    'Maxim Tomato' : 12,
    '1up' : 13,
    'Invincibility Candy' : 14
}
KNIDL_BASE_ID = 2742740
ITEM_NAME_TO_ID = {
    k:ITEM_TABLE_READABLE[k]+KNIDL_BASE_ID for k in ITEM_TABLE_READABLE.keys()
}

#Here to make a weighted choice from among the filler items
#TODO: make dependent on some sort of master data table to eliminate possible name conflicts
Filler_Items = ['Pep Drink','Maxim Tomato','1up','Invincibility Candy']
Filler_Weights = [4,2,3,1] #These are not the in-game ratios, I just made them up. In the future, this will probably be an option

# Each Item instance must correctly report the "game" it belongs to.
# To make this simple, it is common practice to subclass the basic Item class and override the "game" field.
class KirbyNIDLItem(Item):
    game = "Kirby Nightmare in Dream Land"

# The world must be able to create arbitrary amounts of filler as requested by core.
# To do this, it must define a function called world.get_filler_item_name(), which we will define in world.py later.
# This function will help define that required function
def get_random_filler_item_name(world: KirbyNIDLWorld) -> str:
    # IMPORTANT: Whenever you need to use a random generator, we must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # NEVER use a bare random object from Python's built-in random module.
    return world.random.choices(Filler_Items,Filler_Weights,k=1)[0]

# Our world class must have a create_item() function that can create any of our items FROM NAME at any time.
# So, we make this helper function that creates the item by name with the correct classification.
# As in APQuest it's probably to have it in its own function over here in items.py.
def create_classified_item(world: KirbyNIDLWorld, name: str) -> KirbyNIDLItem:
    #Decide on the correct classification (this will probably be neater and more systematic later)
    classification = None
    if 'Level Key' in name:
        classification = ItemClassification.progression
    if name in Filler_Items:
        classification = ItemClassification.filler
    if name == 'Star Rod Piece':
        classification = ItemClassification.progression
    #note that you can assign two classifications at once with "|" like this, useful in logic (mainly useful + prog or useful + filler)
    #In Kirby NIDL, all abilities will be useful, most but not all will also be prog
    ##classification = ItemClassification.progression | ItemClassification.useful
    
    return KirbyNIDLItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

#This function will actually create all the items
#According to AP spec, there must be exactly as many items created as locations
#Filler solves it when locations > items
#But on certain settings (if we decide to make them options), there may be more items than locations, 
#in which point that option set is invalid, but that's later
def create_all_items(world: KirbyNIDLWorld) -> None:
    # Creating items should generally be done via the world's create_item method.
    # First, create a list containing all the items that always exist (depending on options (later))
    #For now, this is the 4 door keys and the star rod piece
    #Eventually, do this via the master item structure
    itempool: list[Item] = [
        ##No Keys at the moment, maybe no keys ever
        # #world.create_item("Vegetable Valley 1 Level Key"), #This needs to be given in starting inventory (randomize which of the 4 is open later)
        # world.create_item("Vegetable Valley 2 Level Key"),
        # world.create_item("Vegetable Valley 3 Level Key"),
        # world.create_item("Vegetable Valley 4 Level Key"),
        world.create_item("Star Rod Piece"),
    ]

    #Now find how much filler to place
    #First use this handy helper function (note that since no locations are filled yet, this is all the fillable locations)
    #You could also do len(world.get_locations()), but this would include the "Fake" even locations
    n_locs = len(world.multiworld.get_unfilled_locations(world.player))
    n_filler = n_locs - len(itempool)

    #Don't do this if the World has a specific set of filler items, but since filler is arbitrary in KirbyNIDL, this is fine
    #create_filler will use the "get random filler item name" function that we made above, eventually
    itempool += [world.create_filler() for _ in range(n_filler)]
    #Final statement to place in World object
    world.multiworld.itempool += itempool
    #Apparently, this is also the best place to give the player starting items via this function below
    #Which we (would) need to do in Kirby here to give the player a starting level (if level keys were implemented)
    #world.push_precollected(world.create_item("Vegetable Valley 1 Level Key"))