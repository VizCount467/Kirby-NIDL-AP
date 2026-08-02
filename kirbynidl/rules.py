from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .world import KirbyNIDLWorld
#See locations for explanation of this boilerplate

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

# In order for AP to generate an item layout that is actually possible for the player to complete,
# we need to define rules for our Entrances and Locations.
# NOTE: Regions do not have rules, the Entrances connecting them do!
# We'll do entrances first, then locations, and then finally we set our victory condition.
def set_all_rules(world: KirbyNIDLWorld) -> None:
    #Or, we would set entrance rules, if we didn't set them all (the door key rules) back in regions.py
    #We still need the W1 -> W2 connection rules, but that comes later
    #If we were to define entrance rules, it would look like this:
    ## entrance = world.get_entrance("entrance_name")
    ## set_rule(entrance,some_function_callable_with_state)
    #set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: KirbyNIDLWorld) -> None:
    #Now location rules will be run thousands or millions of time in a gen, so this is the ONE part of the code that
    #should be as optimized as possible. This means, put as little logic in the rule itself as possible (mainly, this means
    # evaluating conditions involve player options OUTSIDE the rule)
    # Using lambdas with boolean logic combos of state.has and state.has_all is standard
    #you can also AND rules together via add_rule(location,rule) once one rule is set, but this is actually slower and not recommended
    
    #Now, since the entrance rules handle all door key logic in NiDL, all we need to set is the logic for pickups outside of the keys (abilities, et)
    #And also the boss logic (star rod pieces)
    #For now, no pickup in world 1 requires an ability, so let's just set the boss rule
    set_rule(world.get_location("Vegetable Valley - Boss (Whispy Woods)"),
              lambda state: state.has("Star Rod Piece", world.player)
              )
    #Also set the rule for the victory event (duplicate of whispy, for now)
    set_rule(world.get_location("Final Boss Defeated"),
              lambda state: state.has("Star Rod Piece", world.player)
              )

# Finally, we need to set a completion condition for our world, defining what the player needs to win the game.
# This would be the minimum requirements to beat the final boss, but it's a little cleaner to use a "victory event"
def set_completion_condition(world: KirbyNIDLWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)