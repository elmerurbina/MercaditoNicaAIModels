import unittest
from unittest.mock import patch
import pandas as pd
from data.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    @patch('data.data_loader.requests.get')
    def test_load_data(self, mock_get):
        mock_get.return_value.json.return_value = [
            {"feature1": 1, "feature2": 2, "target_column": 3},
            {"feature1": 4, "feature2": 5, "target_column": 6}
        ]
        data_loader = DataLoader(api_url='http://test-api-url', target_column='target_column')
        data = data_loader.get_data()
        self.assertEqual(len(data), 2)
        self.assertIn('feature1', data.columns)
        self.assertIn('target_column', data.columns)

    def test_preprocess_data(self):
        # Mock data to simulate preprocessing
        data = pd.DataFrame({
            'feature1': [1, 2, 3],
            'feature2': [4, 5, 6],
            'target_column': [1, 0, 1]
        })
        data_loader = DataLoader(api_url='http://test-api-url', target_column='target_column')
        data_loader.data = data  # Directly setting data for testing
        cleaned_data = data_loader.preprocess_data(data)
        self.assertFalse(cleaned_data.duplicated().any())
        self.assertNotIn('object', cleaned_data.dtypes)
        self.assertTrue(all(cleaned_data.select_dtypes(include=['float64']).min().ge(0)))
        self.assertIn('feature1', cleaned_data.columns)
        self.assertIn('target_column', cleaned_data.columns)

    def test_split_data(self):
        # Mock data for splitting
        data = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': [5, 6, 7, 8],
            'target_column': [1, 0, 1, 0]
        })
        data_loader = DataLoader(api_url='http://test-api-url', target_column='target_column')
        data_loader.data = data  # Directly setting data for testing
        data_loader.cleaned_data = data_loader.preprocess_data(data)
        X_train, X_test, y_train, y_test = data_loader.split_data()
        self.assertEqual(X_train.shape[0] + X_test.shape[0], data_loader.get_data().shape[0])
        self.assertEqual(y_train.shape[0] + y_test.shape[0], data_loader.get_data().shape[0])

if __name__ == '__main__':
    unittest.main()
