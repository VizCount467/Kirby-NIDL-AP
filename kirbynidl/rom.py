from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple
import io, os, bsdiff4

import Utils
from worlds.Files import APProcedurePatch
#from BaseClasses import MultiWorld
from settings import get_settings
import settings

class KirbyNIDLPatch(APProcedurePatch):
    game = "Kirby Nightmare in Dream Land"
    hash = "35ae64b0f27e60107c14ab956f6cdf70"
    patch_file_ending = ".apknidl"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["data/KNDL_AP_v0.bsdiff"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

def get_base_rom_as_bytes() -> bytes:
    file_name = get_settings().KNIDL_Settings['rom_file']
    file_path = Path(file_name)
    if not file_path.exists():
        file_path = Path(Utils.user_path(file_name))
        if not file_path.exists():
            raise FileNotFoundError("No valid ROM file selected.")
        
    with file_path.open('rb') as infile: 
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes

class KirbyNIDLSettings(settings.Group):
    class KirbyNIDLRomFile(settings.UserFilePath):
        """File name of your US Kirby Nightmare in Dream Land ROM"""
        required = True
        description = "Kirby Nightmare in Dream Land ROM File"
        copy_to = "Kirby Nightmare in Dream Land (USA).gba"
        md5s = ["35ae64b0f27e60107c14ab956f6cdf70"] #Please note this is a LIST of valid hashes (ie, for different localizations or versions)

    rom_file: KirbyNIDLRomFile = KirbyNIDLRomFile("Kirby Nightmare in Dream Land (USA).gba")
    rom_start: bool = True

