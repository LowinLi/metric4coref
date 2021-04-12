"""
@author: longweili
单元测试
"""
import unittest
from src import get_f1, muc, ceaf, b_cubed

clusters1 = [["a", "b", "c"], ["d", "e", "f", "g"], ["h", "i", "j"]]
clusters2 = [["a", "b", "d"], ["d", "e", "c", "g"], ["h", "i", "j", "k"]]


class Tests(unittest.TestCase):
    def test_f1(self):
        self.assertAlmostEqual(get_f1(0.8, 0.9), 0.8470588)

    def test_muc(self):
        p, r, f = muc(clusters1, clusters2)
        print(p, r, f)

    def test_b_cubed(self):
        p, r, f = b_cubed(clusters1, clusters2)
        print(p, r, f)

    def test_ceaf(self):
        p, r, f = ceaf(clusters1, clusters2)
        print(p, r, f)
