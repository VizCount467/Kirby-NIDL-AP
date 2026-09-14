from .bases import KNIDLTestBase
from ..regions import WORLD_NAMES_INDEXED

class TestBasic(KNIDLTestBase):
    #Inside of a Test Class, we can set whatever world options. Options unspecified will use their default values
    options = {
        'pieces_in_pool': 7,
        'req_pieces_num' : 7,
        'req_pieces_prc' : 0
    }

    #Default test will also be run for every test file. According to APQuest, these are:
    #if you have every item, you can access every location
    #if you have no items, you can reach something (Sphere 1 has locations)
    #The world successfully generates

    def test_adhoc(self) -> None:
        with self.subTest('Test adhoc: W3 Boss requires 3 pieces'):
            loc = self.world.get_location('Butter Building - Boss (Mr. Shine and Mr. Bright)')
            self.assertFalse(loc.can_reach(self.multiworld.state))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.collect(self.get_item_by_name('Star Rod Piece'))
            self.assertTrue(loc.can_reach(self.multiworld.state))

    #test functions must start with "test" (I think?)
    def test_basic_access(self) -> None:
        #Inside the Test Function, we can manually collect items and check access rules based on the collection state
        with self.subTest("Test 7 piece World Progression"): #Can we beat the first level of World N with N-1 Pieces and not access the next world?
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
