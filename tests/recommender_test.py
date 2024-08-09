import unittest
from unittest.mock import patch, Mock
import pandas as pd
from models.recommender import Recommender


class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.django_api_base_url = 'http://mock-django-api'
        self.recommender = Recommender(self.django_api_base_url)

    @patch('requests.get')
    def test_get_user_data(self, mock_get):
        # Mock response for user data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'interests': ['eco-friendly', 'sustainable'],
            'location': {'latitude': 12.34, 'longitude': 56.78}
        }
        mock_get.return_value = mock_response

        interests, location = self.recommender.get_user_data(user_id=1)
        self.assertEqual(interests, ['eco-friendly', 'sustainable'])
        self.assertEqual(location, (12.34, 56.78))

    @patch('requests.get')
    def test_get_product_data(self, mock_get):
        # Mock response for product data
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'id': 1, 'description': 'Eco-friendly water bottle', 'latitude': 12.34, 'longitude': 56.78, 'price': 10.0,
             'rating': 4.5},
            {'id': 2, 'description': 'Sustainable notebook', 'latitude': 23.45, 'longitude': 67.89, 'price': 5.0,
             'rating': 4.0}
        ]
        mock_get.return_value = mock_response

        products_df = self.recommender.get_product_data()
        expected_df = pd.DataFrame([
            {'id': 1, 'description': 'Eco-friendly water bottle', 'latitude': 12.34, 'longitude': 56.78, 'price': 10.0,
             'rating': 4.5},
            {'id': 2, 'description': 'Sustainable notebook', 'latitude': 23.45, 'longitude': 67.89, 'price': 5.0,
             'rating': 4.0}
        ])
        pd.testing.assert_frame_equal(products_df, expected_df)

    @patch('recommender.Recommender.get_user_data')
    @patch('recommender.Recommender.get_product_data')
    @patch('recommender.Recommender.calculate_similarity')
    @patch('recommender.geodesic')
    def test_recommend(self, mock_geodesic, mock_calculate_similarity, mock_get_product_data, mock_get_user_data):
        # Mock user data
        mock_get_user_data.return_value = (['eco-friendly'], (12.34, 56.78))

        # Mock product data
        mock_get_product_data.return_value = pd.DataFrame([
            {'id': 1, 'description': 'Eco-friendly water bottle', 'latitude': 12.34, 'longitude': 56.78, 'price': 10.0,
             'rating': 4.5},
            {'id': 2, 'description': 'Sustainable notebook', 'latitude': 23.45, 'longitude': 67.89, 'price': 5.0,
             'rating': 4.0}
        ])

        # Mock similarity calculation
        mock_calculate_similarity.return_value = [0.8, 0.6]

        # Mock geodesic distance
        mock_geodesic.return_value = Mock(kilometers=10)

        recommendations = self.recommender.recommend(user_id=1)
        expected_df = pd.DataFrame([
            {'id': 1, 'description': 'Eco-friendly water bottle', 'latitude': 12.34, 'longitude': 56.78, 'price': 10.0,
             'rating': 4.5, 'similarity': 0.8, 'distance': 10},
            {'id': 2, 'description': 'Sustainable notebook', 'latitude': 23.45, 'longitude': 67.89, 'price': 5.0,
             'rating': 4.0, 'similarity': 0.6, 'distance': 10}
        ])
        pd.testing.assert_frame_equal(recommendations, expected_df)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
