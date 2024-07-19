import unittest
import pandas as pd
from models.market_analysis import MarketAnalysis
from models.pricing import PricingCalculator
from models.recommender import Recommender

class TestMarketAnalysis(unittest.TestCase):
    def setUp(self):
        self.api_url = 'http://your-api-url'  # Reemplaza con la URL real de la API
        self.analysis = MarketAnalysis(self.api_url)

    def test_fetch_data(self):
        df = self.analysis.fetch_data(user_id=1)
        self.assertGreater(len(df), 0, "La longitud del DataFrame debe ser mayor a 0")
        self.assertIn('amount', df.columns, "El DataFrame debe contener la columna 'amount'")

    def test_process_data(self):
        df = pd.DataFrame({
            'date': ['2024-07-01'],
            'hour': ['14:30:00'],
            'amount': [100],
            'buyer_location': [{'latitude': 12.34, 'longitude': 56.78}]
        })
        processed_df = self.analysis.process_data(df)
        self.assertIn('hour', processed_df.columns, "El DataFrame procesado debe contener la columna 'hour'")
        self.assertIn('sales_amount', processed_df.columns, "El DataFrame procesado debe contener la columna 'sales_amount'")

    def test_generate_statistics(self):
        df = pd.DataFrame({
            'date': pd.to_datetime(['2024-07-01']),
            'hour': [14],
            'sales_amount': [100],
            'buyer_latitude': [12.34],
            'buyer_longitude': [56.78]
        })
        daily_sales, hourly_sales, location_sales = self.analysis.generate_statistics(df)
        self.assertGreater(daily_sales.sum(), 0, "La suma de ventas diarias debe ser mayor a 0")
        self.assertGreater(hourly_sales.sum(), 0, "La suma de ventas por hora debe ser mayor a 0")
        self.assertGreater(len(location_sales), 0, "Debe haber datos de ventas por ubicación")

class TestPricingCalculator(unittest.TestCase):
    def setUp(self):
        self.product_id = 1
        self.calculator = PricingCalculator(self.product_id)

    def test_fetch_product_data(self):
        # Llama a la API real aquí
        self.calculator.fetch_product_data()
        self.assertIsNotNone(self.calculator.material_cost_per_unit, "El costo del material por unidad no debe ser None")
        self.assertIsNotNone(self.calculator.transport_cost, "El costo de transporte no debe ser None")

    def test_calculate_total_cost(self):
        self.calculator.material_cost_per_unit = 10
        self.calculator.quantity_per_unit = 5
        self.calculator.transport_cost = 20
        self.calculator.labor_cost = 30
        self.calculator.material_costs = 25
        self.calculator.other_expenses = 10
        total_cost = self.calculator.calculate_total_cost()
        self.assertGreater(total_cost, 0, "El costo total debe ser mayor a 0")

    def test_suggest_price(self):
        self.calculator.material_cost_per_unit = 10
        self.calculator.quantity_per_unit = 5
        self.calculator.transport_cost = 20
        self.calculator.labor_cost = 30
        self.calculator.material_costs = 25
        self.calculator.other_expenses = 10
        suggested_price, earnings_percentage = self.calculator.suggest_price()
        self.assertGreater(suggested_price, 0, "El precio sugerido debe ser mayor a 0")

class TestRecommender(unittest.TestCase):
    def setUp(self):
        self.django_api_base_url = 'http://your-django-api-url'  # Reemplaza con la URL real de la API
        self.recommender = Recommender(self.django_api_base_url)

    def test_get_user_data(self):
        interests, location = self.recommender.get_user_data(user_id=1)
        self.assertIsNotNone(interests, "Los intereses del usuario no deben ser None")
        self.assertIsNotNone(location, "La ubicación del usuario no debe ser None")

    def test_get_product_data(self):
        df = self.recommender.get_product_data()
        self.assertGreater(len(df), 0, "La longitud del DataFrame de productos debe ser mayor a 0")
        self.assertIn('name', df.columns, "El DataFrame de productos debe contener la columna 'name'")

    # Aquí podrías agregar más pruebas para el método `recommend` si tienes una implementación más detallada

if __name__ == '__main__':
    unittest.main()
