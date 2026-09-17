from .bases import KNIDLTestBase
from ..regions import WORLD_NAMES_INDEXED

class TestPiecesRemainder(KNIDLTestBase):
    options = {
        'pieces_in_pool': 10,
        'req_pieces_num' : 10,
        'req_pieces_prc' : 0,
    }
    def test_pieces_remainder(self) -> None:
        with self.subTest('Basic Progression Test, but ensure 10 pieces needed for final with 10 required'):
            loc = self.world.get_location('Vegetable Valley 1 - Level Clear')
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Ice Cream Island 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Butter Building 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state)) #Apparently, we CAN reach 3-1 with only 1 star piece??
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state)) 

            loc = self.world.get_location('Grape Garden 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Yogurt Yard 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Orange Ocean 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Rainbow Resort 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('The Fountain of Dreams - Nightmare')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece')) #7/10
            self.assertFalse(loc.can_reach(self.multiworld.state))

            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece')) #10/10
            self.assertTrue(loc.can_reach(self.multiworld.state))

class TestPiecesMax56(KNIDLTestBase):
    options = {
        'pieces_in_pool': 56,
        'req_pieces_num' : 56,
        'req_pieces_prc' : 0,
    }
    def test_56_req_pieces(self) -> None:
        with self.subTest('Basic Progression Test, but with max piece count (56)'):
            loc = self.world.get_location('Vegetable Valley 1 - Level Clear')
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Ice Cream Island 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece')) 
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Butter Building 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state)) 

            loc = self.world.get_location('Grape Garden 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Yogurt Yard 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece')) 
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Orange Ocean 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece')) 
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Rainbow Resort 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece')) 
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('The Fountain of Dreams - Nightmare')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            for _ in range(8):
                self.collect(self.get_item_by_name('Star Rod Piece')) 
            self.assertTrue(loc.can_reach(self.multiworld.state))

class TestPiecesExcess(KNIDLTestBase):
    options = {
        'pieces_in_pool': 20,
        'req_pieces_num' : 10,
        'req_pieces_prc' : 0,
    }
    def test_pieces_excess(self) -> None:
        with self.subTest('Basic Progression Test, but ensure everything works with 10 pieces req, 20 in pool'):
            loc = self.world.get_location('Vegetable Valley 1 - Level Clear')
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Ice Cream Island 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Butter Building 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state)) #Apparently, we CAN reach 3-1 with only 1 star piece??
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state)) 

            loc = self.world.get_location('Grape Garden 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Yogurt Yard 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Orange Ocean 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Rainbow Resort 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('The Fountain of Dreams - Nightmare')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece')) #7/10
            self.assertFalse(loc.can_reach(self.multiworld.state))

            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece')) #10/10
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece')) #13/10
            self.assertTrue(loc.can_reach(self.multiworld.state))

class TestPiecesPercent(KNIDLTestBase):
    options = {
        'pieces_in_pool': 14,
        'req_pieces_num' : 47,
        'req_pieces_prc' : 50,
    }
    def test_pieces_remainder(self) -> None:
        with self.subTest('Basic Progression Test, but with 50 percent of 14 pieces required'):
            loc = self.world.get_location('Vegetable Valley 1 - Level Clear')
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Ice Cream Island 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Butter Building 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state)) #Apparently, we CAN reach 3-1 with only 1 star piece??
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state)) 

            loc = self.world.get_location('Grape Garden 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Yogurt Yard 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Orange Ocean 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('Rainbow Resort 1 - Level Clear')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

            loc = self.world.get_location('The Fountain of Dreams - Nightmare')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece')) #7/10
            self.assertTrue(loc.can_reach(self.multiworld.state))
