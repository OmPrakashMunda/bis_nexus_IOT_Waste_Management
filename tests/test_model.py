import unittest
import pandas as pd
from ai.model import WasteManagementAI

class TestWasteManagementAI(unittest.TestCase):
    def setUp(self):
        self.ai = WasteManagementAI('../data/bhubaneswar_waste_data.csv')

    def test_predict_collections(self):
        bins = self.ai.predict_collections()
        self.assertIsInstance(bins, np.ndarray)
        self.assertTrue(len(bins) > 0)

    def test_optimize_route(self):
        bins = self.ai.predict_collections()
        route = self.ai.optimize_route(bins)
        self.assertEqual(len(route), len(bins))

if __name__ == '__main__':
    unittest.main()