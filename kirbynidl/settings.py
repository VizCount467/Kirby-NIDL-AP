import settings

class KirbyNIDLSettings(settings.Group):
    class KirbyNIDLRomFile(settings.UserFilePath):
        """File name of your US Kirby Nightmare in Dream Land ROM"""
        required = True
        description = "Kirby Nightmare in Dream Land ROM File"
        copy_to = "Kirby Nightmare in Dream Land (USA).gba"
        md5s = "35ae64b0f27e60107c14ab956f6cdf70"

    rom_file: KirbyNIDLRomFile = KirbyNIDLRomFile(KirbyNIDLRomFile.copy_to)
    rom_start: bool = True

