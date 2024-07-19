import requests

class PricingCalculator:
    def __init__(self, product_id):
        """
        Inicializa el calculador de precios con datos obtenidos desde el API de Django.

        :param product_id: ID del producto para obtener datos
        """
        self.product_id = product_id
        self.product_data = self.fetch_product_data()
        self.material_cost_per_unit = self.product_data['material_cost_per_unit']
        self.quantity_per_unit = self.product_data['quantity_per_unit']
        self.price_per_unit = self.product_data['price_per_unit']
        self.transport_cost = self.product_data['transport_cost']
        self.labor_cost = self.product_data['labor_cost']
        self.material_costs = self.product_data['material_costs']
        self.other_expenses = self.product_data['other_expenses']
        self.earnings_percentage = self.product_data.get('earnings_percentage')

    def fetch_product_data(self):
        """
        Obtiene datos del producto desde el API de Django.

        :return: Datos del producto
        """
        url = f'http://<django-backend-url>/api/products/{self.product_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error al obtener los datos del producto")

    def calculate_total_cost(self):
        """
        Calcula el costo total del producto.

        :return: Costo total del producto
        """
        material_cost_total = self.material_cost_per_unit * self.quantity_per_unit
        total_cost = (
            material_cost_total + self.transport_cost + self.labor_cost + self.material_costs + self.other_expenses)
        return total_cost

    def estimate_earnings_percentage(self, total_cost):
        """
        Estima el porcentaje de ganancia basado en el costo total del producto.

        :param total_cost: Costo total del producto
        :return: Porcentaje de ganancia
        """
        if self.earnings_percentage is not None:
            return self.earnings_percentage
        if total_cost <= 200:
            return 10
        elif total_cost <= 800:
            return 15
        elif total_cost <= 1500:
            return 20
        else:
            return 25

    def suggest_price(self):
        """
        Sugiere un precio para el producto basado en el costo total y el porcentaje de ganancia estimado.

        :return: Precio sugerido para el producto
        """
        total_cost = self.calculate_total_cost()
        earnings_percentage = self.estimate_earnings_percentage(total_cost)
        suggested_price = total_cost * (1 + earnings_percentage / 100)

        return suggested_price, earnings_percentage

    def generate_price_suggestion_message(self):
        """
        Genera un mensaje cordial y amigable con la sugerencia de precio.

        :return: Mensaje de sugerencia de precio
        """
        suggested_price, earnings_percentage = self.suggest_price()
        return (f"Hola, basado en los datos proporcionados, el precio sugerido para su producto es "
                f"${suggested_price:.2f}. Esto incluye un margen de ganancia de {earnings_percentage}% sobre el costo total del producto. "
                "Este precio le permitirá cubrir todos los gastos y obtener una ganancia adecuada. "
                "¡Esperamos que esta sugerencia le sea útil para su negocio!")

# Ejemplo de uso
if __name__ == "__main__":
    product_id = 1  # Asumimos que el ID del producto es 1
    calculator = PricingCalculator(product_id)
    print(calculator.generate_price_suggestion_message())
