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
        for rn in region_names:
            if rn.startswith(world_name + ' '):
                r = world.get_region(rn)
                w.connect(r, rn + " Door") 

    #Connect all world regions to each other in sequence with Star Rod Pieces as the requirement
    #Do the Star Rod calculation from options
    if world.options.req_pieces_prc == 0:
        req_pieces = world.options.req_pieces_num
    else:
        req_pieces = int(world.options.req_pieces_prc/100 * world.options.pieces_in_pool)
    if req_pieces > world.options.pieces_in_pool:
        raise Exception('Error in Star Rod Piece Options: number of required pieces cannot be greater than amount in pool')
    if req_pieces < 7:
        raise Exception('Error in Received Star Rod Piece Options: number of required pieces is less than 7 (percent set too low)')
    #Calculate the required pieces for each boss
    req_pieces_per_boss = int(req_pieces/7)

    for i, world_name in enumerate(WORLD_NAMES_INDEXED[:-1]):
        w_current = world.get_region(world_name)
        w_next = world.get_region(WORLD_NAMES_INDEXED[i+1])
        req_pieces_i = req_pieces_per_boss*(i+1)
        ##PYTHON PITFALL: if a lambda references iteration variable i, it will "look up" the value of i when called, which is the END VALUE of the loop (ie, 6)
        ##SOLUTION: use the extra "rp" variable in the lambda with the "req pieces" value defined in the loop. Notice how the "rp" var turns color in VS code
        ##This applies to ALL rule functions
        w_current.connect(w_next,world_name + ' Next Door', lambda state, rp=req_pieces_i: state.has("Star Rod Piece", world.player, rp))
    


  
