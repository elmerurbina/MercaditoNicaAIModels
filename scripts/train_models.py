import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, SVC
import joblib
from models.model_utils import preprocess_data


def fetch_data_from_api(api_url):
    """
    Obtiene datos desde una API y los devuelve como un DataFrame.

    :param api_url: URL del API para obtener datos
    :return: DataFrame con los datos obtenidos
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        raise Exception("Error al obtener los datos desde el API")


def train_regression_models(api_url, target_column):
    """
    Entrena varios modelos de regresión usando los datos obtenidos desde la API y guarda los modelos entrenados.

    :param api_url: URL del API para obtener datos
    :param target_column: Nombre de la columna objetivo
    """
    # Cargar y preprocesar los datos
    df = fetch_data_from_api(api_url)
    X_train, X_test, y_train, y_test = preprocess_data(df, target_column)

    # Definir modelos
    models = {
        'RandomForestRegressor': RandomForestRegressor(n_estimators=100, max_depth=10),
        'LinearRegression': LinearRegression(),
        'SVR': SVR()
    }

    for model_name, model in models.items():
        # Entrenar el modelo
        model.fit(X_train, y_train)

        # Guardar el modelo
        joblib.dump(model, f'models/{model_name}.pkl')
        print(f"Modelo {model_name} entrenado y guardado como models/{model_name}.pkl")


def train_classification_models(api_url, target_column):
    """
    Entrena varios modelos de clasificación usando los datos obtenidos desde la API y guarda los modelos entrenados.

    :param api_url: URL del API para obtener datos
    :param target_column: Nombre de la columna objetivo
    """
    # Cargar y preprocesar los datos
    df = fetch_data_from_api(api_url)
    X_train, X_test, y_train, y_test = preprocess_data(df, target_column)

    # Definir modelos
    models = {
        'RandomForestClassifier': RandomForestClassifier(n_estimators=100, max_depth=10),
        'LogisticRegression': LogisticRegression(),
        'SVC': SVC()
    }

    for model_name, model in models.items():
        # Entrenar el modelo
        model.fit(X_train, y_train)

        # Guardar el modelo
        joblib.dump(model, f'models/{model_name}.pkl')
        print(f"Modelo {model_name} entrenado y guardado como models/{model_name}.pkl")


if __name__ == "__main__":
    # Configuración de URLs y columnas
    api_url_regression = 'http://localhost:8000/api/regression-data/'  # URL del API para datos de regresión
    api_url_classification = 'http://localhost:8000/api/classification-data/'  # URL del API para datos de clasificación
    target_column_regression = 'target'  # Nombre de la columna objetivo para regresión
    target_column_classification = 'target'  # Nombre de la columna objetivo para clasificación

    print("Entrenando modelos de regresión...")
    train_regression_models(api_url_regression, target_column_regression)

    print("\nEntrenando modelos de clasificación...")
    train_classification_models(api_url_classification, target_column_classification)
