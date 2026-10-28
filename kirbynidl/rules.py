from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations for explanation of this boilerplate
from .locations import LOCATION_TABLE_READABLE
from .regions import WORLD_NAMES_INDEXED

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

#Table of abilities mapped to the earliest world they can be obtained in the vanilla game
ABILITY_AVAILABILITY_TABLE = {
    'Beam' : 1,
    'Spark' : 1,
    'Fire' : 1,
    'Cutter' : 1,
    'Burning' : 1,
    'Sword' : 1,
    'Freeze' : 1,
    'Needle' : 1,
    'Crash' : 1,
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

ABILITIES_IN_ALL_WORLDS = set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash'])
#If ability in ABILITIES_IN_ALL_WORLDS or ABILITY_AVAILABILITY_TABLE[ability] == 1

#List of abilities in each world, indexed to each world, ie 'Laser' in ABILITIES_IN_WORLD[1] -> True
ABILITIES_IN_WORLD = [
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Needle','Freeze']),
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Laser','Wheel','Parasol','Needle','Hi-Jump','Stone','Tornado']), #Also freeze, but only in the arena. A fact irrelevent unless we do world shuffle
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Laser','Wheel','Hammer','Parasol','Needle','Ice','Freeze','Hi-Jump','Stone']),
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Laser','Wheel','Parasol','Freeze','Stone','Tornado','Throw']),
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Parasol','Laser','Stone','Hammer','Wheel','Hi-Jump','Needle','Ice']),
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Parasol','Laser','Stone','Hammer','Hi-Jump','Needle','Ice','Freeze','Tornado','Throw']),
    set(['Fire','Spark','Cutter','Sword','Burning','Beam','Crash','Parasol','Laser','Stone','Hammer','Wheel','Freeze','Tornado','Throw'])
]

#Similar to above. Only relevant for Tornado (W5) and Wheel (W6) at this point
ABILITIES_IN_MUSEUM = [
    set(['Sword']),
    set(['Laser','Fire']),
    set(['Hi-Jump']),
    set(['Sleep','Ball']),
    set(['Stone','Tornado']),
    set(['Wheel']),
    set([])
]

#lambda state: state.can_reach_region("Egypt", player)

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
    #Location rules will be run thousands or millions of time in a gen, so this is the ONE part of the code that
    #should be as optimized as possible. This means, put as little logic in the rule itself as possible (mainly, this means
    #evaluating conditions involving player options OUTSIDE the rule)
    # Using lambdas with boolean logic combos of state.has and state.has_all is standard
    #you can also AND rules together via add_rule(location,rule) once one rule is set, but this is actually slower and not recommended

    #Some helper functions for abilities. Needed since you can have an ability unlocked, but not be able to reach a world where you can access it
    #req_pieces is a local variable to set "set all location rules" function. Hoping this is fine efficiency-wise. May not need it with new region-based function?
    def can_use_ability(state, world, ability):
        #Short-circuit not having the ability unlocked at all
        if not state.has(ability, world.player):
                return False
        if ABILITY_AVAILABILITY_TABLE[ability] == 1 or ability in ABILITIES_IN_ALL_WORLDS:
                #W1 abilities are always available if unlocked. For abilities in all worlds, we can also short-circuit the logic
                return True
        else:
                #Check if player has access to any world with ability
                can_access_world = False
                for i in range(7):
                    if state.can_reach_region(WORLD_NAMES_INDEXED[i],world.player) and ability in ABILITIES_IN_WORLD[i]:
                        can_access_world = True
                        break
                if can_access_world:
                        return True
                #Check the niche cases of W5 Tornado and W6 Wheel via Museum. W2 Freeze via Arena would also be here, but that's a W1 ability
                if ability == 'Tornado' and state.has('Yogurt Yard Museum Key') and state.can_reach_region('Yogurt Yard'):
                        return True
                if ability == 'Wheel' and state.has('Orange Ocean Museum Key') and state.can_reach_region('Orange Ocean'):
                        return True

    def can_use_any_ability(state,world,ability_list):
        return any([can_use_ability(state,world,ability) for ability in ability_list])

    def can_pound_stake(state,world):
        return can_use_any_ability(state,world,('Stone','Hammer'))

    if world.options.advanced_logic:
        def can_light_fuse(state,world):
                return can_use_any_ability(state,world,('Fire','Burning','Laser','Crash'))
    else:
        def can_light_fuse(state,world):
                return can_use_any_ability(state,world,('Fire','Burning','Laser'))

    def can_destroy_metal_side(state,world):
        return can_use_any_ability(state, world,  ('Burning','Wheel','Hammer'))
    
    #Now, since the entrance rules handle all Star Rod Pieces, all we need to set is the logic for ability use
    #And also the boss checks, since those take place in world X, but require X Star Rod pieces
    #These follow a pattern, so we can do them systematically
    #Calculate the number of required pieces
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
        for loc_name in LOCATION_TABLE_READABLE.keys():
            if 'Boss' in loc_name and world_name in loc_name:
                req_pieces_i = req_pieces_per_boss*(i+1)
                set_rule(world.get_location(loc_name),
                        lambda state, rp=req_pieces_i: state.has("Star Rod Piece", world.player, rp) #see regions.py for explanation of the "rp" variable
                        )
                break
    #For all other location rules, there are no real patterns. So, everything will just be manual, I guess
    ###LEVEL PICKUP LOGIC
    set_rule(world.get_location("Ice Cream Island 3 - Tomato (UFO Room)"),
             lambda state, : can_use_any_ability(state, world,  (
                 'Beam','Spark','Burning','Sword','Freeze','Needle','Hi-Jump','Parasol','Hammer'
             )))
    
    if world.options.advanced_logic:
        set_rule(world.get_location("Ice Cream Island 3 - 1up (Cave Ceiling Passage)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Burning','Sword','Freeze','Needle','Hi-Jump','Parasol','Hammer','Wheel'
                )) 
                or state.has('UFO',world.player)
                or can_use_ability(state, world, 'Throw')
                )
        set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 1)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
                ))
                or can_use_ability(state,world,'Cutter')
                )
        set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 2)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
                ))
                or can_use_ability(state,world,'Cutter')
        )
        set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 3)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
                ))
                or can_use_ability(state,world,'Cutter')
                )
    else:
        set_rule(world.get_location("Ice Cream Island 3 - 1up (Cave Ceiling Passage)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Burning','Sword','Freeze','Needle','Hi-Jump','Parasol','Hammer','Wheel'
                )) 
                or state.has('UFO',world.player)
                )
        set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 1)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
                )))
        set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 2)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
                )))
        set_rule(world.get_location("Ice Cream Island 4 - Pep Drink (Laser Room 3)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw'
                )))

    set_rule(world.get_location("Ice Cream Island 4 - 1up (Laser Room 4)"),
            lambda state, : can_use_any_ability(state, world,  (
                'Beam','Spark','Fire','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Ice','Throw','Wheel'
            )))
    if not world.options.advanced_logic: #following checks can be obtained with no abilities by use of double star
        set_rule(world.get_location("Ice Cream Island 5 - 1up (Metal Blocks 1)"),
                lambda state, : can_destroy_metal_side(state,world)
                or can_use_ability(state,world,'Throw')
                )
        set_rule(world.get_location("Ice Cream Island 5 - 1up (Metal Blocks 2)"),
                lambda state, : can_destroy_metal_side(state,world)
                or can_use_ability(state,world,'Throw')
                )
    if world.options.advanced_logic:
        set_rule(world.get_location("Ice Cream Island 5 - 1up (Gordo Guarded)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Burning','Tornado','Wheel'
                )))
    else:
        set_rule(world.get_location("Ice Cream Island 5 - 1up (Gordo Guarded)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Burning','Tornado'
                )))
    
    set_rule(world.get_location("Butter Building 5 - Tomato (Stake Room 1)"),
            lambda state, : can_pound_stake(state,world))
    set_rule(world.get_location("Butter Building 5 - 1up (Stake Room 2)"),
            lambda state, : can_pound_stake(state,world))
    
    set_rule(world.get_location("Grape Garden 3 - 1up (Cannon Reward)"),
            lambda state, : can_light_fuse(state,world))
    set_rule(world.get_location("Grape Garden 4 - 1up (Wheel Race)"),
            lambda state, : can_use_ability(state, world,  'Wheel'))
    set_rule(world.get_location("Grape Garden 5 - 1up (Burning Room Bottom)"),
            lambda state, : can_use_ability(state, world,  'Burning'))
    set_rule(world.get_location("Grape Garden 6 - 1up (Stake Room)"),
            lambda state, : can_pound_stake(state,world))

    set_rule(world.get_location("Yogurt Yard 3 - Tomato (Stake Room Left)"),
            lambda state, : can_pound_stake(state,world))
    set_rule(world.get_location("Yogurt Yard 3 - 1up (Stake Room Right)"),
            lambda state, : can_pound_stake(state,world))
    if world.options.advanced_logic:
        set_rule(world.get_location("Yogurt Yard 4 - 1up (Spike Tunnel)"),
                lambda state, : can_use_any_ability(state, world,  ('Burning','Tornado')))
    else:
        set_rule(world.get_location("Yogurt Yard 4 - 1up (Spike Tunnel)"),
                lambda state, : can_use_ability(state, world,  'Burning'))
    set_rule(world.get_location("Yogurt Yard 6 - 1up (Big Switch Room Left)"),
            lambda state, : can_use_ability(state, world,  'Hammer'))

    set_rule(world.get_location("Orange Ocean 1 - 1up (Metal Blocks)"),
            lambda state, : can_destroy_metal_side(state,world)
            or can_use_ability(state,world,'Throw')
            )
    if not world.options.advanced_logic: #another set where a double star makes them obtainable without abilities
        set_rule(world.get_location("Orange Ocean 3 - Pep Drink (Bonkers Room)"),
                lambda state, : can_destroy_metal_side(state,world)
                or can_use_ability(state,world,'Throw')
                )
        set_rule(world.get_location("Orange Ocean 3 - 1up (Man Overboard!)"),
                lambda state, : can_destroy_metal_side(state,world)
                or can_use_ability(state,world,'Throw')
                )
        set_rule(world.get_location("Orange Ocean 3 - Tomato (Laser Ball Room)"),
                lambda state, : can_destroy_metal_side(state,world)
                or can_use_ability(state,world,'Throw')
                )
    set_rule(world.get_location("Orange Ocean 4 - 1up (Beam Bomb Block 1)"),
            lambda state, : can_use_ability(state, world,  'Beam'))
    set_rule(world.get_location("Orange Ocean 4 - 1up (Beam Bomb Block 2)"),
            lambda state, : can_use_ability(state, world,  'Beam'))
    set_rule(world.get_location("Orange Ocean 4 - 1up (Beam Bomb Block 3)"),
            lambda state, : can_use_ability(state, world,  'Beam'))
    if not world.options.advanced_logic: #double star
        set_rule(world.get_location("Orange Ocean 6 - 1up (Upper Path Metal Blocks)"),
                lambda state, : can_destroy_metal_side(state,world)
                or state.has('UFO',world.player)
                )
    if world.options.advanced_logic: #advanced logic enables cutter and wheel
        set_rule(world.get_location("Rainbow Resort 1 - 1up (Laser Room)"),
                lambda state, : can_use_any_ability(state, world,  (
                        'Beam','Spark','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Throw','Cutter','Wheel'
                )))
    else:
        set_rule(world.get_location("Rainbow Resort 1 - 1up (Laser Room)"),
                   lambda state, : can_use_any_ability(state, world,  (
                           'Beam','Spark','Burning','Sword','Freeze','Needle','Laser','Hi-Jump','Parasol','Hammer','Throw'
                   )))
        #7-5 Cannon: On base logic, Fire AND Burning; player can use whichever they're best at. On Advanced, either, and also Crash
    if not world.options.advanced_logic:
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 1)"),
                lambda state, : can_use_ability(state, world,  'Fire') and can_use_ability(state, world,  'Burning'))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 2)"),
                lambda state, : can_use_ability(state, world,  'Fire') and can_use_ability(state, world,  'Burning'))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 3)"),
                lambda state, : can_use_ability(state, world,  'Fire') and can_use_ability(state, world,  'Burning'))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 4)"),
                lambda state, : can_use_ability(state, world,  'Fire') and can_use_ability(state, world,  'Burning'))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 5)"),
                lambda state, : can_use_ability(state, world,  'Fire') and can_use_ability(state, world,  'Burning'))
    else:
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 1)"),
                lambda state, : can_use_any_ability(state, world, ('Fire','Crash','Burning')))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 2)"),
                lambda state, : can_use_any_ability(state, world, ('Fire','Crash','Burning')))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 3)"),
                lambda state, : can_use_any_ability(state, world, ('Fire','Crash','Burning')))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 4)"),
                lambda state, : can_use_any_ability(state, world, ('Fire','Crash','Burning')))
        set_rule(world.get_location("Rainbow Resort 5 - 1up (Cannon Reward 5)"),
                lambda state, : can_use_any_ability(state, world, ('Fire','Crash','Burning')))

    ###BIG SWITCH LOGIC
    #Technically, the 4-6 big switch is free if you know where it is, but no new player would find it without the intended strat
    set_rule(world.get_location("Grape Garden 6 - Big Switch"),
        lambda state, : state.has("Light", world.player)
        )
    if world.options.advanced_logic:
        set_rule(world.get_location("Yogurt Yard 5 - Big Switch"),
                lambda state, : 
                #Condition 1: any fuse lighter (that's not Crash) and Hi-Jump
                (can_use_any_ability(state, world, ('Fire','Laser')) and can_use_ability(state, world, 'Hi-Jump')
                ) or
                #Condition 2: Burning
                (can_use_ability(state, world, 'Burning')
                ) or
                #Condition 3: Any of a set of abilities that can break the blocks and Fire. Advanced allows parasol, which is fairly tricky
                (can_use_ability(state,world,'Fire') and can_use_any_ability(state,world,(
                        'Spark','Sword','Freeze','Needle','Hammer','Throw','Parasol'
                ))
                )
        )
    else:
        set_rule(world.get_location("Yogurt Yard 5 - Big Switch"),
                lambda state, : 
                (can_use_any_ability(state, world, ('Fire','Laser')) and can_use_ability(state, world, 'Hi-Jump')
                ) or
                (can_use_ability(state, world, 'Burning')
                ) or
                (can_use_ability(state,world,'Fire') and can_use_any_ability(state,world,(
                        'Spark','Sword','Freeze','Needle','Hammer','Throw'
                ))
                )
        )
    set_rule(world.get_location("Yogurt Yard 6 - Big Switch"),
            lambda state, : can_use_ability(state, world,  'Hammer'))
    
    set_rule(world.get_location("Orange Ocean 1 - Big Switch"), #Break metal block below
        lambda state, : can_use_any_ability(state, world,  ('Wheel','Hammer','Stone')))
    set_rule(world.get_location("Orange Ocean 2 - Big Switch"),
        lambda state, : can_pound_stake(state,world))
    if world.options.advanced_logic:
        set_rule(world.get_location("Orange Ocean 3 - Big Switch"),
                lambda state, : can_use_ability(state, world,  'Laser'))
    else:
        set_rule(world.get_location("Orange Ocean 3 - Big Switch"),
                lambda state, : can_use_ability(state, world,  'Laser') 
                and (
                        can_destroy_metal_side(state,world)
                        or can_use_ability(state,world,'Throw')
                ))
    set_rule(world.get_location("Orange Ocean 5 - Big Switch"),
                lambda state, : can_light_fuse(state,world))
    if world.options.advanced_logic:
        set_rule(world.get_location("Orange Ocean 6 - Big Switch"), #Break metal block over gap
                        lambda state, : can_use_any_ability(state,world,('Burning','Wheel','Hammer'))
                        or state.has("UFO", world.player)
                )
        set_rule(world.get_location("Rainbow Resort 1 - Big Switch"), #Break rock blocks on ceiling, THEN side metal in same room. 
                        lambda state, : can_use_ability(state,world,'Hammer') or can_use_ability(state,world,'Burning'))
    else:
        set_rule(world.get_location("Orange Ocean 6 - Big Switch"), #Break metal block over gap
                        lambda state, : can_use_ability(state,world,'Burning')
                        or state.has("UFO", world.player)
                )
        set_rule(world.get_location("Rainbow Resort 1 - Big Switch"), 
                        lambda state, : can_use_ability(state,world,'Hammer') or can_use_ability(state,world,'Burning'))


    ##Arenas Logic
    for w in WORLD_NAMES_INDEXED[1:-1]: #only worlds 2-6 have Arenas
        set_rule(world.get_location(f"{w} - Arena Clear"),
                lambda state, wn=w: state.has(f'{wn} Arena Key', world.player))

    
    #Also set the rule for the victory event
    set_rule(world.get_location("The Fountain of Dreams - Nightmare"),
              lambda state, rp=req_pieces: state.has("Star Rod Piece", world.player, rp)
              )

# Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
# This would be the minimum requirements to beat the final boss, but it's a little cleaner to use a "victory event"
def set_completion_condition(world: KirbyNIDLWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)