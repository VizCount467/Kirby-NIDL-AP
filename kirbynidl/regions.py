from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations.py for explanation of this boilerplate

from BaseClasses import Region #,Entrance

#TODO: greater abstraction when we make the full list
region_names = ["Vegetable Valley","Vegetable Valley 1","Vegetable Valley 2","Vegetable Valley 3","Vegetable Valley 4"]

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
    w1 = world.get_region("Vegetable Valley")
    w1_names_to_regions = {rn:world.get_region(rn) for rn in region_names if rn.startswith("Vegetable Valley ")} #space to get all levels and not the world itself
    for rn in w1_names_to_regions.keys():
        #region (region object), entrance name (string), rule definition with state
        #remember that a lambda is just a nameless function; any callable function could fill the arg also (but an argument of a "state" object is expected, ofc)
        ##w1.connect(w1_names_to_regions[rn], rn + " Door", lambda state: state.has(rn + " Level Key", world.player)) ##Key rule dummied out until keys implemented, maybe never
        w1.connect(w1_names_to_regions[rn], rn + " Door")
  
