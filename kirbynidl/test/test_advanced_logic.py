from .bases import KNIDLTestBase
from ..regions import WORLD_NAMES_INDEXED

class TestAdvLogicOff(KNIDLTestBase):
    options = {
        'pieces_in_pool': 7,
        'req_pieces_num' : 7,
        'req_pieces_prc' : 0,
        'advanced_logic' : False
    }

    def test_adv_logic_off(self) -> None:
        with self.subTest('Test if 2-3 Cave 1up is impossible with only Throw and Advanced Logic off'):
            for _ in range(7):
                self.collect(self.get_item_by_name('Star Rod Piece')) ##unlock all levels
            loc = self.world.get_location('Ice Cream Island 3 - 1up (Cave Tunnel)')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Throw'))
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Needle'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

class TestAdvLogicOn(KNIDLTestBase):
    options = {
        'pieces_in_pool': 7,
        'req_pieces_num' : 7,
        'req_pieces_prc' : 0,
        'advanced_logic' : True
    }

    def test_adv_logic_off_1(self) -> None:
        with self.subTest('Test if 2-2 Cave 1up is possible with only Throw and Advanced Logic on'):
            for _ in range(3):
                self.collect(self.get_item_by_name('Star Rod Piece')) ##unlock world 4
            loc = self.world.get_location('Ice Cream Island 3 - 1up (Cave Tunnel)')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Throw'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

    def test_adv_logic_off_2(self) -> None:
        with self.subTest('Ice Cream Island 4 - Pep Drink (Laser Room 3)'):
            for _ in range(1):
                self.collect(self.get_item_by_name('Star Rod Piece')) ##unlock world 2
            loc = self.world.get_location('Ice Cream Island 4 - Pep Drink (Laser Room 3)')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Cutter'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

    def test_adv_logic_off_3(self) -> None:
        with self.subTest('Ice Cream Island 5 - 1up (Metal Blocks 1)'):
            for _ in range(1):
                self.collect(self.get_item_by_name('Star Rod Piece')) ##unlock world 2
            loc = self.world.get_location('Ice Cream Island 5 - 1up (Metal Blocks 1)')
            self.assertTrue(loc.can_reach(self.multiworld.state))

            
    