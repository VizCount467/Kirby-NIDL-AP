from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations for explanation of this boilerplate
from .locations import LOCATION_TABLE_READABLE
from .regions import WORLD_NAMES_INDEXED

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

#Table of abilities mapped to the earlier world they can be obtained in the vanilla game
ABILITY_AVAILABILITY_TABLE = {
    'Beam' : 1,
    'Spark' : 1,
    'Fire' : 1,
    'Cutter' : 1,
    'Burning' : 1,
    'Sword' : 1,
    'Freeze' : 1,
    'Needle' : 1,
    'Laser' : 2,
    'Hi-Jump' : 2,
    'Parasol' : 2,
    'Stone' : 2,
    'Tornado' : 2,
    'Wheel' : 2,
    'Backdrop' : 3,
    'Hammer' : 3,
    'Ice' : 3,
    'Ball' : 4,
    'Throw' : 4
}

#Some helper functions for abilities. Needed since you can have an ability unlocked, but not be able to reach a world where you can access it
#Relies on Star Rod requirements for World being fixed -- do note
def can_use_ability(state, world, ability):
    return state.has(ability, world.player) and state.has('Star Rod Piece', world.player, ABILITY_AVAILABILITY_TABLE[ability])

def can_use_any_ability(state,world,ability_list):
    return any([can_use_ability(state,world,ability) for ability in ability_list])

def can_pound_stake(state,world):
    return can_use_any_ability(state,world,('Stone','Hammer'))

def can_light_fuse(state,world):
    return can_use_any_ability(state,world,('Fire','Burning','Laser'))

def can_destroy_metal_side(state,world):
    return can_use_any_ability(state, world, ('Burning','Wheel','Hammer'))


Advanced_Logic = True #TODO: replace this with a toggle option later. For now, it's just always on

# In order for AP to generate an item layout that is actually possible for the player to complete,
# we need to define rules for our Entrances and Locations.
# NOTE: Regions do not have rules, the Entrances connecting them do!
def set_all_rules(world: KirbyNIDLWorld) -> None:
    #Or, we would set entrance rules, if we didn't set them all (the door key rules) back in regions.py
    #If we were to define entrance rules, it would look like this:
    ## entrance = world.get_entrance("entrance_name")
    ## set_rule(entrance,some_function_callable_with_state)
    #set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: KirbyNIDLWorld) -> None:
    #Now location rules will be run thousands or millions of time in a gen, so this is the ONE part of the code that
    #should be as optimized as possible. This means, put as little logic in the rule itself as possible (mainly, this means
    #evaluating conditions involving player options OUTSIDE the rule)
    # Using lambdas with boolean logic combos of state.has and state.has_all is standard
    #you can also AND rules together via add_rule(location,rule) once one rule is set, but this is actually slower and not recommended
    
    #Now, since the entrance rules handle all Star Rod Pieces, all we need to set is the logic for ability use
    #And also the boss checks, since those take place in world X, but require X Star Rod pieces
    #These follow a pattern, so we can do them systematically
    for i, world_name in enumerate(WORLD_NAMES_INDEXED[:-1]):
        for loc_name in LOCATION_TABLE_READABLE.keys():
            if 'Boss' in loc_name and world_name in loc_name:
                set_rule(world.get_location(loc_name),
                        lambda state: state.has("Star Rod Piece", world.player, i)
                        )
                break
    #For all other location rules, there are no real patterns. So, everything will just be manual, I guess
    ###LEVEL PICKUP LOGIC
    set_rule(world.get_location("Ice Cream Island 3 - Tomato (UFO Room)"),
             lambda state: can_use_any_ability(state, world, (
                 'Beam','Spark','Burning','Sword','Freeze','Needle','Hi-Jump','Parasol','Hammer'
             ))
             )
    set_rule(world.get_location("Ice Cream Island 3 - 1up (Cave Tunnel)"),
            lambda state: can_use_any_ability(state, world, (
                'Beam','Spark','Burning','Sword','Freeze','Needle','Hi-Jump','Parasol','Hammer','Wheel'
            )) 
            or state.has('UFO',world.player)
            or (Advanced_Logic and can_use_ability(state, world,'Throw'))
            )
    set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 1)"),
            lambda state: can_use_any_ability(state, world, (
                'Beam','Spark','Fire','Cutter','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
            )))
    set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 2)"),
            lambda state: can_use_any_ability(state, world, (
                'Beam','Spark','Fire','Cutter','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
            )))
    set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 3)"),
            lambda state: can_use_any_ability(state, world, (
                'Beam','Spark','Fire','Cutter','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
            )))
    set_rule(world.get_location("Ice Cream Island 4 - 1up (Laser Room 4)"),
            lambda state: can_use_any_ability(state, world, (
                'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw','Wheel'
            )))
    set_rule(world.get_location("Ice Cream Island 5 - 1up (Metal Blocks 1)"),
            lambda state: can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            or Advanced_Logic #Double star
            )
    set_rule(world.get_location("Ice Cream Island 5 - 1up (Metal Blocks 2)"),
            lambda state: can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            or Advanced_Logic
            )
    set_rule(world.get_location("Ice Cream Island 5 - 1up (Gordo Guarded)"),
            lambda state: can_use_any_ability(state, world, (
                'Burning','Tornado'
            ))
            or (Advanced_Logic and can_use_ability(state, world,'Wheel'))
            )
    
    set_rule(world.get_location("Butter Building 5 - Tomato (After Bonkers 1)"),
            lambda state: can_pound_stake(state,world))
    set_rule(world.get_location("Butter Building 5 - 1up (After Bonkers 2)"),
            lambda state: can_pound_stake(state,world))
    
    set_rule(world.get_location("Grape Garden 3 - 1up (Cannon)"),
            lambda state: can_light_fuse(state,world))
    set_rule(world.get_location("Grape Garden 4 - 1up (Wheel Race)"),
            lambda state: can_use_ability(state, world, 'Wheel'))
    set_rule(world.get_location("Grape Garden 5 - 1up (Burning Room Bottom)"),
            lambda state: can_use_ability(state, world, 'Burning'))
    set_rule(world.get_location("Grape Garden 6 - 1up (Stake)"),
            lambda state: can_pound_stake(state,world))

    set_rule(world.get_location("Yogurt Yard 3 - Tomato (Stake Room Left)"),
            lambda state: can_pound_stake(state,world))
    set_rule(world.get_location("Yogurt Yard 3 - 1up (Stake Room Right)"),
            lambda state: can_pound_stake(state,world))
    set_rule(world.get_location("Yogurt Yard 4 - 1up (Spike Tunnel)"),
            lambda state: can_use_ability(state, world, 'Burning'))
    set_rule(world.get_location("Yogurt Yard 6 - 1up (Big Switch Room Left)"),
            lambda state: can_use_ability(state, world, 'Hammer'))

    set_rule(world.get_location("Orange Ocean 1 - 1up (Metal Blocks)"),
            lambda state: can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            )
    set_rule(world.get_location("Orange Ocean 3 - Pep Drink (Bonkers Room)"),
            lambda state: can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            or Advanced_Logic #Double star
            )
    set_rule(world.get_location("Orange Ocean 3 - 1up (Man Overboard!)"),
            lambda state: can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            or Advanced_Logic #Double star
            )
    set_rule(world.get_location("Orange Ocean 3 - Tomato (Laser Ball Room)"),
            lambda state: can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            or Advanced_Logic #Double star
            )
    set_rule(world.get_location("Orange Ocean 4 - 1up (Beam Bomb Block 1)"),
            lambda state: can_use_ability(state, world, 'Beam'))
    set_rule(world.get_location("Orange Ocean 4 - 1up (Beam Bomb Block 2)"),
            lambda state: can_use_ability(state, world, 'Beam'))
    set_rule(world.get_location("Orange Ocean 4 - 1up (Beam Bomb Block 3)"),
            lambda state: can_use_ability(state, world, 'Beam'))
    set_rule(world.get_location("Orange Ocean 6 - 1up (Upper Path Metal Blocks)"),
            lambda state: can_destroy_metal_side(state,world)
            or state.has('UFO',world.player)
            or Advanced_Logic #Double star
            )
    
    set_rule(world.get_location("Rainbow Resort 1 - 1up (Laser Room)"),
            lambda state: can_use_any_ability(state, world, (
                'Beam','Spark','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Throw'
            ))
            or (Advanced_Logic and can_use_ability(state,world,'Cutter'))
            or (Advanced_Logic and can_use_ability(state,world,'Wheel'))
            )
    set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 1)"),
            lambda state: can_use_ability(state, world, 'Fire'))
    set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 2)"),
            lambda state: can_use_ability(state, world, 'Fire'))
    set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 3)"),
            lambda state: can_use_ability(state, world, 'Fire'))
    set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 4)"),
            lambda state: can_use_ability(state, world, 'Fire'))
    set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 5)"),
            lambda state: can_use_ability(state, world, 'Fire'))

    ###BIG SWITCH LOGIC
    #Technically, the 4-6 big switch is free if you know where it is, but no new player would find it without the intended strat
    set_rule(world.get_location("Grape Garden 6 - Big Switch"),
        lambda state: can_use_ability(state, world, 'Light'))
    set_rule(world.get_location("Yogurt Yard 5 - Big Switch"),
        lambda state: can_light_fuse(state,world)
        and can_use_ability(state, world,'Hi-Jump')
        )
    set_rule(world.get_location("Yogurt Yard 6 - Big Switch"),
            lambda state: can_use_ability(state, world, 'Hammer'))
    
    set_rule(world.get_location("Orange Ocean 1 - Big Switch"), #Break metal block below
        lambda state: can_use_any_ability(state, world, ('Wheel','Hammer','Stone')))
    set_rule(world.get_location("Orange Ocean 2 - Big Switch"),
        lambda state: can_pound_stake(state,world))
    set_rule(world.get_location("Orange Ocean 3 - Big Switch"),
        lambda state: can_use_ability('Laser') and (
        can_destroy_metal_side(state,world)
        or can_use_ability(state,world,'Throw')
        or Advanced_Logic) #Double star
        )
    set_rule(world.get_location("Orange Ocean 5 - Big Switch"),
        lambda state: can_light_fuse(state,world))
    set_rule(world.get_location("Orange Ocean 6 - Big Switch"), #Break metal block over gap
            lambda state: can_use_ability(state,world,'Burning')
            or can_use_ability(state,world,'UFO')
            or (Advanced_Logic and can_use_any_ability(state,world,('Wheel','Hammer')))
    )
    set_rule(world.get_location("Rainbow Resort 1 - Big Switch"), #Break rock blocks on ceiling, THEN side metal in same room. Most complex logic of any location
            lambda state: can_use_ability(state,world,'Hammer') or (
                can_use_ability(state,world,'Burning') and (
                        can_use_any_ability(state,world,('Beam','Spark','Burning','Sword','Freeze','Hi-Jump','Parasol'))
                        or Advanced_Logic and can_use_any_ability(state,world,('Fire','Ice','Needle'))
                )
            )
    )

    ##Arenas Logic
    for w in WORLD_NAMES_INDEXED[1:-1]: #only worlds 2-6 have Arenas
        set_rule(world.get_location(f"{w} - Arena Clear"),
                lambda state: state.has(f'{w} Arena Key', world.player))

    
    #Also set the rule for the victory event
    set_rule(world.get_location("The Fountain of Dreams - Nightmare"),
              lambda state: state.has("Star Rod Piece", world.player,7)
              )

# Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
# This would be the minimum requirements to beat the final boss, but it's a little cleaner to use a "victory event"
def set_completion_condition(world: KirbyNIDLWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)