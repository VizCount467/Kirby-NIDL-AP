##init.py -- this thing runs first, obviously. Following APQuest, we're going to init the world
from .world import KirbyNIDLWorld as KirbyNIDLWorld
from .client import KirbyNIDLClient #though we don't use the client in this level of the code, this line is required to get AP to recognize the patch file

