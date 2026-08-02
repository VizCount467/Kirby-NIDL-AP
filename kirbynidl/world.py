##world.py -- implements the AP World class, which is the master Class for the generation
from collections.abc import Mapping
from typing import Any, ClassVar
import pkgutil, os
# Imports of base Archipelago modules must be absolute.
from worlds.AutoWorld import World

# Imports of your world's files must be relative.
from . import items, locations, regions, rules, web_world, rom, settings
from . import options as kirbynidl_options  # rename due to a name conflict with World.options



class KirbyNIDLWorld(World):
    """
    Kirby Nightmare in Dream Land is the GBA remake of the classic Kirby's Adventure on the NES
    Venture through seven varied worlds, copy the unique abilities of your enemies, 
    and collect the pieces of the Star Rod to restore the Fountain of Dreams.
    """
    # This docstring will be displayed on the WebHost. Typically a fun, "back of the box" description of what happens in the game

    game = "Kirby Nightmare in Dream Land" #well duh
    web = web_world.KirbyNIDLWebWorld() #webworld goes here

    #Options go here with our world.
    # This is how we associate the options defined in our options.py with our world.
    options_dataclass = kirbynidl_options.KirbyNIDLOptions
    options: kirbynidl_options.KirbyNIDLOptions #This is just a type hint, but it's probably required by the APWorld system

    #Seemingly required to get meta generation settings to work and such?
    settings_key = "KNIDL_Settings"
    settings: ClassVar[settings.KirbyNIDLSettings]

    # The World class must have a static location_name_to_id and item_name_to_id, those names exactly.
    # We define these in regions.py and items.py respectively, just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    #In NiDL, we can just use the region representing the World 1 OW
    origin_region_name = "Vegetable Valley"

    # Our world class must have certain functions ("steps") that get called during generation.
    # The main ones are: create_regions, set_rules, create_items.
    # For better structure and readability, we have put each of these in their own file, and we invoke them here
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)
    
    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    def create_item(self, name: str) -> items.KirbyNIDLItem:
        return items.create_classified_item(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # For this purpose we defined a function in items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    #Needed for the client to have access to any player-controlled options
    def fill_slot_data(self) -> Mapping[str, Any]:
        # If you need access to the player's chosen options on the client side, there is a helper for that.
        return self.options.as_dict(
            "lock_bonus_doors", "lock_copy_abilities", "randomize_pickups", "starting_vitality","max_vitality"
        )

    #Is this function being called?
    def generate_output(self, output_directory: str) -> None:
        
        patch = rom.KirbyNIDLPatch(player=self.player, player_name=self.player_name)
        patch.write_file("data/KNDL_AP_v0.bsdiff", pkgutil.get_data(__name__, "data/KNDL_AP_v0.bsdiff"))
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))