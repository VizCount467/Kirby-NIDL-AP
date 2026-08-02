from pathlib import Path
import Utils
from typing import TYPE_CHECKING, List, Tuple
import io, os, bsdiff4

from worlds.Files import APProcedurePatch
from BaseClasses import MultiWorld
from .settings import KirbyNIDLSettings

class KirbyNIDLPatch(APProcedurePatch):
    game = "Kirby Nightmare in Dream Land"
    hash = "35ae64b0f27e60107c14ab956f6cdf70"
    patch_file_ending = ".apkirbynidl"
    result_file_ending = ".gba"

    procedure = [
        ("apply_bsdiff4", ["data/KNDL_AP_v0.bsdiff"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

def get_base_rom_as_bytes() -> bytes:
    file_name = KirbyNIDLSettings.rom_file
    file_path = Path(file_name)
    if not file_path.exists():
        file_path = Path(Utils.user_path(file_name))
        if not file_path.exists():
            raise FileNotFoundError("No valid ROM file selected.")
        
    with file_path.open('rb') as infile: 
        base_rom_bytes = bytes(infile.read())

    return base_rom_bytes

