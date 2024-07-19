import pandas as pd
from geopy.distance import geodesic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests


class Recommender:
    def __init__(self, django_api_base_url):
        """
        Inicializa el recomendador con configuraciones predeterminadas.

        :param django_api_base_url: URL base de la API del backend de Django
        """
        self.vectorizer = TfidfVectorizer(stop_words='spanish')
        self.api_base_url = django_api_base_url

    def get_user_data(self, user_id):
        """
        Obtiene los intereses y la ubicación del usuario desde la API de Django.

        :param user_id: ID del usuario
        :return: Tuple (interests, location)
        """
        url = f'{self.api_base_url}/api/userprofiles/{user_id}/'
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            interests = user_data['interests']
            location = (user_data['location']['latitude'], user_data['location']['longitude'])
            return interests, location
        else:
            raise Exception("Error al obtener los datos del usuario")

    def get_product_data(self):
        """
        Obtiene todos los datos de productos desde la API de Django.

        :return: DataFrame de productos
        """
        url = f'{self.api_base_url}/api/products/'
        response = requests.get(url)
        if response.status_code == 200:
            products = response.json()
            return pd.DataFrame(products)
        else:
            raise Exception("Error al obtener los datos de los productos")

    def recommend(self, user_id, top_n=5):
        """
        Recomienda productos basados en el ID del usuario.

        :param user_id: ID del usuario
        :param top_n: Número máximo de recomendaciones a devolver (por defecto 5)
        :return: DataFrame de productos recomendados
        """
        interests, user_location = self.get_user_data(user_id)
        products_df = self.get_product_data()

        # Filtrar productos según intereses
        filtered_products = self.filter_by_interests(products_df, interests)

        # Calcular similitudes de productos
        filtered_products['similarity'] = self.calculate_similarity(filtered_products['description'])

        # Calcular distancias desde la ubicación del usuario
        filtered_products['distance'] = filtered_products.apply(
            lambda row: geodesic(user_location, (row['latitude'], row['longitude'])).kilometers,
            axis=1
        )

        # Filtrar productos con mejor puntuación
        filtered_products['rating'] = filtered_products.get('rating', [0] * len(
            filtered_products))  # Asume una columna de rating opcional
        filtered_products = filtered_products.sort_values(by=['rating'], ascending=False)

        # Ordenar productos por similitud, luego por distancia, luego por precio
        recommended_products = filtered_products.sort_values(by=['similarity', 'distance', 'price'])

        # Seleccionar los primeros N productos
        return recommended_products.head(top_n)

    def filter_by_interests(self, products_df, interests):
        """
        Filtra productos basados en los intereses del usuario.

        :param products_df: DataFrame de productos
        :param interests: Lista de intereses
        :return: DataFrame filtrado
        """
        interests = set(interests)
        return products_df[products_df['description'].apply(
            lambda desc: any(interest in desc for interest in interests)
        )]

    def calculate_similarity(self, descriptions):
        """
        Calcula la similitud coseno de las descripciones de productos.

        :param descriptions: Serie de descripciones de productos
        :return: Puntajes de similitud
        """
        descriptions_matrix = self.vectorizer.fit_transform(descriptions)
        return cosine_similarity(descriptions_matrix[0:1], descriptions_matrix).flatten()


# Ejemplo de uso
if __name__ == "__main__":
    django_api_base_url = 'http://<django-backend-url>' #URL de la API desarrollada en Django
    recommender = Recommender(django_api_base_url)
    user_id = 1  # ID del usuario de ejemplo

    recommendations = recommender.recommend(user_id)
    print(recommendations)
