# tests/test_ai_model.py
import unittest
import numpy as np
from ai.model import WasteManagementAI

class TestWasteManagementAI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        cls.ai = WasteManagementAI('data/bhubaneswar_waste_data.csv')
        # Train the model before running tests
        cls.metrics = cls.ai.train_models()

    def test_model_initialization(self):
        """Test if the model is properly initialized."""
        self.assertIsNotNone(self.ai.fill_predictor)
        self.assertIsNotNone(self.ai.data)
        self.assertTrue(self.ai.is_trained)

    def test_train_models(self):
        """Test model training and metrics."""
        self.assertIn('train_score', self.metrics)
        self.assertIn('test_score', self.metrics)
        self.assertGreater(self.metrics['train_score'], 0)
        self.assertGreater(self.metrics['test_score'], 0)

    def test_predict_collections(self):
        """Test collection predictions."""
        bins = self.ai.predict_collections()
        self.assertIsInstance(bins, np.ndarray)
        self.assertTrue(len(bins) >= 0)  # Should return at least empty array
        if len(bins) > 0:
            self.assertTrue(all(isinstance(x, (int, np.integer)) for x in bins))

    def test_optimize_route(self):
        """Test route optimization."""
        # Test with empty bins
        empty_route = self.ai.optimize_route(np.array([]))
        self.assertEqual(len(empty_route), 0)

        # Test with actual bins
        bins = self.ai.predict_collections()
        route = self.ai.optimize_route(bins)
        self.assertEqual(len(route), len(bins))
        self.assertTrue(all(bin_id in bins for bin_id in route))

    def test_data_loading(self):
        """Test data loading and preprocessing."""
        required_columns = {'bin_id', 'timestamp', 'fill_level', 'temperature', 
                          'humidity', 'waste_type', 'collection_frequency'}
        self.assertTrue(all(col in self.ai.data.columns for col in required_columns))
        self.assertFalse(self.ai.data.empty)

if __name__ == '__main__':
    unittest.main(verbosity=2)