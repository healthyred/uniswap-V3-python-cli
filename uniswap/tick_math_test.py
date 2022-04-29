from re import I
import tick_math
import unittest

class TestTickMath(unittest.TestCase):

    def msb_test(self):
        for i in range(1,256):
            x = 2 ** i
            self.assertTrue(tick_math.most_significant_bit(x) == i)

    def nearest_usable_tick_test(self):

        # throws if tickSpacing is 0.
        self.assertRaises('TICK_SPACING', tick_math.nearest_usable_tick(1, 0))
