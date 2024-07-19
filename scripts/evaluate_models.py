import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR, SVC
from models.model_utils import preprocess_data, calculate_metrics, calculate_classification_metrics


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


def train_and_evaluate_regression_models(api_url, target_column):
    """
    Entrena y evalúa varios modelos de regresión usando los datos obtenidos desde la API.

    :param api_url: URL del API para obtener datos
    :param target_column: Nombre de la columna objetivo
    :return: Resultados de evaluación para cada modelo
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

    results = {}

    for model_name, model in models.items():
        # Entrenar el modelo
        model.fit(X_train, y_train)

        # Realizar predicciones
        y_pred = model.predict(X_test)

        # Calcular métricas
        metrics = calculate_metrics(y_test, y_pred)
        results[model_name] = metrics

    return results


def train_and_evaluate_classification_models(api_url, target_column):
    """
    Entrena y evalúa varios modelos de clasificación usando los datos obtenidos desde la API.

    :param api_url: URL del API para obtener datos
    :param target_column: Nombre de la columna objetivo
    :return: Resultados de evaluación para cada modelo
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

    results = {}

    for model_name, model in models.items():
        # Entrenar el modelo
        model.fit(X_train, y_train)

        # Realizar predicciones
        y_pred = model.predict(X_test)

        # Calcular métricas
        metrics = calculate_classification_metrics(y_test, y_pred)
        results[model_name] = metrics

    return results


if __name__ == "__main__":
    # Configuración de URLs y columnas
    api_url_regression = 'http://localhost:8000/api/regression-data/'  # URL del API para datos de regresión
    api_url_classification = 'http://localhost:8000/api/classification-data/'  # URL del API para datos de clasificación
    target_column_regression = 'target'  # Nombre de la columna objetivo para regresión
    target_column_classification = 'target'  # Nombre de la columna objetivo para clasificación

    print("Evaluando modelos de regresión...")
    regression_results = train_and_evaluate_regression_models(api_url_regression, target_column_regression)
    for model_name, metrics in regression_results.items():
        print(f"Modelo: {model_name}")
        print(f"Métricas: {metrics}")

    print("\nEvaluando modelos de clasificación...")
    classification_results = train_and_evaluate_classification_models(api_url_classification,
                                                                      target_column_classification)
    for model_name, metrics in classification_results.items():
        print(f"Modelo: {model_name}")
        print(f"Métricas: {metrics}")
