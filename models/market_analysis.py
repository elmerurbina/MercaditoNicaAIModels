import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class MarketAnalysis:
    def __init__(self, api_url):
        """
        Inicializa el análisis de mercado con la URL del API.

        :param api_url: URL del API de Django
        """
        self.api_url = api_url

    def fetch_data(self, user_id):
        """
        Obtiene datos de ventas específicos del usuario desde el API de Django.

        :param user_id: ID del usuario
        :return: DataFrame con los datos de ventas
        """
        response = requests.get(f"{self.api_url}/sales/?user_id={user_id}")
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    def process_data(self, df):
        """
        Procesa los datos de ventas para análisis.

        :param df: DataFrame con los datos de ventas
        :return: DataFrame procesado
        """
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = pd.to_datetime(df['hour'], format='%H:%M:%S').dt.hour
        df['sales_amount'] = df['amount'].astype(float)
        df['buyer_latitude'] = df['buyer_location'].apply(lambda loc: loc['latitude'])
        df['buyer_longitude'] = df['buyer_location'].apply(lambda loc: loc['longitude'])
        return df

    def generate_statistics(self, df):
        """
        Genera estadísticas de ventas.

        :param df: DataFrame con los datos de ventas
        :return: DataFrames con estadísticas de ventas
        """
        daily_sales = df.groupby(df['date'].dt.date)['sales_amount'].sum()
        hourly_sales = df.groupby('hour')['sales_amount'].sum()
        location_sales = df.groupby(['buyer_latitude', 'buyer_longitude'])['sales_amount'].sum().reset_index()
        return daily_sales, hourly_sales, location_sales

    def plot_statistics(self, daily_sales, hourly_sales, location_sales):
        """
        Plotea gráficos de las estadísticas de ventas.

        :param daily_sales: Serie con ventas diarias
        :param hourly_sales: Serie con ventas por hora
        :param location_sales: DataFrame con ventas por ubicación
        """
        plt.figure(figsize=(14, 10))

        # Gráfico de ventas diarias
        plt.subplot(3, 1, 1)
        sns.lineplot(x=daily_sales.index, y=daily_sales.values, color='blue')
        plt.title('Ventas Diarias')
        plt.xlabel('Fecha')
        plt.ylabel('Monto de Ventas')

        # Gráfico de ventas por hora
        plt.subplot(3, 1, 2)
        sns.lineplot(x=hourly_sales.index, y=hourly_sales.values, color='green')
        plt.title('Ventas por Hora')
        plt.xlabel('Hora del Día')
        plt.ylabel('Monto de Ventas')

        # Gráfico de ventas por ubicación
        plt.subplot(3, 1, 3)
        plt.figure(figsize=(14, 7))
        sns.scatterplot(x='buyer_longitude', y='buyer_latitude', size='sales_amount', data=location_sales, palette='viridis', sizes=(20, 200))
        plt.title('Ventas por Ubicación del Comprador')
        plt.xlabel('Longitud')
        plt.ylabel('Latitud')

        plt.tight_layout()
        plt.show()

    def run_analysis(self, user_id):
        """
        Ejecuta el análisis de mercado para un usuario específico y muestra los gráficos.

        :param user_id: ID del usuario
        """
        df = self.fetch_data(user_id)
        processed_df = self.process_data(df)
        daily_sales, hourly_sales, location_sales = self.generate_statistics(processed_df)
        self.plot_statistics(daily_sales, hourly_sales, location_sales)


# Ejemplo de uso
if __name__ == "__main__":
    api_url = 'http://<django-backend-url>' #URL de la API desarrollada en Django
    user_id = 1  # ID del usuario de ejemplo
    analysis = MarketAnalysis(api_url)
    analysis.run_analysis(user_id)
