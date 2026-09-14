from test.bases import WorldTestBase

from ..world import KirbyNIDLWorld

class KNIDLTestBase(WorldTestBase):
    game = 'Kirby Nightmare in Dream Land'
    world: KirbyNIDLWorld