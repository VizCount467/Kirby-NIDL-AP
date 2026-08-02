##Webworld: defines how the web page for this game will look, any tutorials, option presets, et.

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

#from .options import option_groups, option_presets

class KirbyNIDLWebWorld(WebWorld):
    game = 'Kirby Nightmare in Dream Land'
    theme = 'grass'

    #Tutorial object: title, description, language, filepath, link, authors
    # The filepath is relative to a "/docs/" directory in the root folder of the apworld.
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Kirby Nightmare in dream Land for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["VizCount"],
    )
    tutorials = [setup_en]

    # If we have option groups and/or option presets, we need to specify these here as well.
    # option_groups = option_groups
    # options_presets = option_presets

    bug_report_page = "my_GH_user_page?"  #TODO: update with GH user page if we publish

    # If we have option groups and/or option presets, we need to specify these here as well.
    #option_groups = option_groups
    #options_presets = option_presets