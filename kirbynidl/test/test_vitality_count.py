from .bases import KNIDLTestBase
from ..regions import WORLD_NAMES_INDEXED

class TestVitality5pc(KNIDLTestBase):
    options = {
        'starting_vitality' : 1,
        'max_vitality' : 6
    }
    def test_vitality_5pc(self) -> None:
        with self.subTest('Test with 1 starting vitality and 6 max, 5 vitality items exist'):
            n_vitalities = self.get_items_by_name("Vitality")
            self.assertEqual(len(n_vitalities), 5)

class TestVitality0pc(KNIDLTestBase):
    options = {
        'starting_vitality' : 3,
        'max_vitality' : 3
    }
    def test_vitality_0pc(self) -> None:
        with self.subTest('Test with 3 starting vitality and 3 max, 0 vitality items exist'):
            n_vitalities = self.get_items_by_name("Vitality")
            self.assertEqual(len(n_vitalities), 0)