from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations.py for explanation of this boilerplate

from BaseClasses import Region #,Entrance

#Helper Table that lists all the worlds in order. Can probably abstract this later
WORLD_NAMES_INDEXED = [
    'Vegetable Valley',
    'Ice Cream Island',
    'Butter Building',
    'Grape Garden',
    'Yogurt Yard',
    'Orange Ocean',
    'Rainbow Resort'
]
#Number of levels in world {[index]+1}
LEVELS_PER_WORLD_INDEX = (4,5,6,6,6,6,6)

region_names = []
for i, world_name in enumerate(WORLD_NAMES_INDEXED):
    region_names.append(world_name)
    for j in range(LEVELS_PER_WORLD_INDEX[i]):
        region_names.append(world_name + ' ' + str(j+1))
#region_names = ["Vegetable Valley","Vegetable Valley 1","Vegetable Valley 2","Vegetable Valley 3","Vegetable Valley 4"] ...

def create_and_connect_regions(world: KirbyNIDLWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: KirbyNIDLWorld) -> None:
    
    #Regions are invoked through their constructor
    knidl_regions = [Region(rn, world.player, world.multiworld) for rn in region_names]
    # We now need to add these regions to multiworld.regions so that AP knows about their existence.
    world.multiworld.regions += knidl_regions

def connect_regions(world: KirbyNIDLWorld) -> None:
    #Connections to region are made by the region.connect helper function
    #You can add a rule to the entrance as the final argument, but this is not required
    #You can also init an entrance object and use entrance.connect(region)
    #Note that entrances are 1-way, but logic assumes you can always get to an earlier if you go to a later region (ie, game reset)

    #Connect all level regions to their parent world region via connections named like "Vegetable Valley 1 Door". These connections have no requirements
    for world_name in WORLD_NAMES_INDEXED:
        w = world.get_region(world_name)
        w_names_to_regions = {rn:world.get_region(rn) for rn in region_names if rn.startswith(world_name + ' ')} #space to get all levels and not the world itself
        for rn in w_names_to_regions.keys():
            #region (region object), entrance name (string), rule definition with state
            #remember that a lambda is just a nameless function; any callable function could fill the arg also (but an argument of a "state" object is expected, ofc)
            ##w1.connect(w1_names_to_regions[rn], rn + " Door", lambda state: state.has(rn + " Level Key", world.player)) 
            w.connect(w_names_to_regions[rn], rn + " Door")

    #Connect all world regions to each other in sequence with Star Rod Pieces as the requirement
    #Currently, the number of Star Rod pieces is fixed
    for i, world_name in enumerate(WORLD_NAMES_INDEXED[:-1]):
        w_current = world.get_region(world_name)
        w_next = world.get_region(WORLD_NAMES_INDEXED[i+1])
        w_current.connect(w_next,world_name + ' Next Door', lambda state: state.has("Star Rod Piece", world.player, i))

  
