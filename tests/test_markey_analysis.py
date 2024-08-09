import unittest
import pandas as pd
from models.market_analysis import MarketAnalysis

class TestMarketAnalysis(unittest.TestCase):

    def setUp(self):
        # Setup a MarketAnalysis instance with a dummy API URL
        self.analysis = MarketAnalysis(api_url='http://dummy-api-url')

    def test_process_data(self):
        # Mock input data with nested dictionary for 'buyer_location'
        input_df = pd.DataFrame({
            'date': ['2024-01-01'],
            'hour': ['14:00:00'],
            'amount': [150.0],
            'buyer_location': [{'latitude': 12.34, 'longitude': 56.78}],
            'sales_amount': [150.0]  # Ensure sales_amount is float
        })

        # Process data
        processed_df = self.analysis.process_data(input_df)

        # Debug prints to inspect DataFrames
        print("Processed DataFrame:")
        print(processed_df)

        # Expected output
        expected_df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-01']),
            'hour': [14],
            'amount': [150.0],
            'buyer_location': [{'latitude': 12.34, 'longitude': 56.78}],
            'sales_amount': [150.0],  # Ensure sales_amount is float
            'buyer_latitude': [12.34],
            'buyer_longitude': [56.78]
        })

        # Convert column data types to match
        processed_df['hour'] = processed_df['hour'].astype('int64')
        processed_df['sales_amount'] = processed_df['sales_amount'].astype('float64')
        expected_df['hour'] = expected_df['hour'].astype('int64')
        expected_df['sales_amount'] = expected_df['sales_amount'].astype('float64')

        # Assert DataFrames are equal considering column order
        pd.testing.assert_frame_equal(processed_df.sort_index(axis=1), expected_df.sort_index(axis=1))

if __name__ == '__main__':
    unittest.main()
