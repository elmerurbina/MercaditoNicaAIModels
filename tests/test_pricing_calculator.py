import unittest
from unittest.mock import patch
from models.pricing import PricingCalculator

class TestPricingCalculator(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_product_data(self, mock_get):
        mock_response = {
            'material_cost_per_unit': 5.0,
            'quantity_per_unit': 100,
            'price_per_unit': 10.0,
            'transport_cost': 50.0,
            'labor_cost': 100.0,
            'material_costs': 200.0,
            'other_expenses': 150.0,
            'earnings_percentage': None
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        calculator = PricingCalculator(product_id=1)
        self.assertEqual(calculator.product_data, mock_response)

    def test_calculate_total_cost(self):
        calculator = PricingCalculator(product_id=1)
        calculator.material_cost_per_unit = 5.0
        calculator.quantity_per_unit = 100
        calculator.transport_cost = 50.0
        calculator.labor_cost = 100.0
        calculator.material_costs = 200.0
        calculator.other_expenses = 150.0

        expected_total_cost = 5.0 * 100 + 50.0 + 100.0 + 200.0 + 150.0
        self.assertEqual(calculator.calculate_total_cost(), expected_total_cost)

    def test_suggest_price(self):
        calculator = PricingCalculator(product_id=1)
        calculator.material_cost_per_unit = 5.0
        calculator.quantity_per_unit = 100
        calculator.transport_cost = 50.0
        calculator.labor_cost = 100.0
        calculator.material_costs = 200.0
        calculator.other_expenses = 150.0

        total_cost = calculator.calculate_total_cost()
        expected_earnings_percentage = calculator.estimate_earnings_percentage(total_cost)
        expected_suggested_price = total_cost * (1 + expected_earnings_percentage / 100)

        suggested_price, earnings_percentage = calculator.suggest_price()
        self.assertEqual(suggested_price, expected_suggested_price)
        self.assertEqual(earnings_percentage, expected_earnings_percentage)

if __name__ == '__main__':
    unittest.main()
