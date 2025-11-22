import unittest
import pandas as pd
import numpy as np
from data_processor import DataProcessor

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.train = pd.DataFrame({'x': [1,2,3], 'y1': [1,4,9]})
        self.ideal = pd.DataFrame({'x': [1,2,3], 'y1': [1,4,9], 'y2': [0,0,0]})

    def test_deviation(self):
        p = DataProcessor(self.train, self.ideal)
        dev = p._deviation(self.train['y1'].values, self.ideal['y1'].values)
        self.assertEqual(dev, 0)

    def test_select_best(self):
        p = DataProcessor(self.train, self.ideal)
        sel = p.select_best_ideal_functions()
        self.assertEqual(sel['y1'][0], 'y1')

if __name__ == '__main__':
    unittest.main()