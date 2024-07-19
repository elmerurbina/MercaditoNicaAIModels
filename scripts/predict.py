import pandas as pd
import requests
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

def load_models(model_names):
    """
    Carga los modelos entrenados desde archivos .pkl.

    :param model_names: Lista de nombres de archivos de modelos
    :return: Diccionario con modelos cargados
    """
    models = {}
    for model_name in model_names:
        models[model_name] = joblib.load(f'models/{model_name}.pkl')
    return models

def predict_with_models(models, X):
    """
    Realiza predicciones usando varios modelos.

    :param models: Diccionario con modelos cargados
    :param X: Datos para hacer predicciones
    :return: Diccionario con predicciones para cada modelo
    """
    predictions = {}
    for model_name, model in models.items():
        predictions[model_name] = model.predict(X)
    return predictions

def save_predictions(predictions, output_file):
    """
    Guarda las predicciones en un archivo CSV.

    :param predictions: Diccionario con predicciones
    :param output_file: Ruta del archivo para guardar las predicciones
    """
    predictions_df = pd.DataFrame(predictions)
    predictions_df.to_csv(output_file, index=False)
    print(f"Predicciones guardadas en {output_file}")

if __name__ == "__main__":
    # Configuración de URLs y modelos
    api_url = 'http://localhost:8000/api/new-data/'  # URL del API para datos nuevos
    model_names = [
        'RandomForestRegressor',
        'LinearRegression',
        'SVR',
        'RandomForestClassifier',
        'LogisticRegression',
        'SVC'
    ]
    output_file = 'predictions.csv'  # Archivo para guardar las predicciones

    # Cargar los modelos
    models = load_models(model_names)

    # Obtener y preprocesar los datos nuevos
    df = fetch_data_from_api(api_url)
    X_new = preprocess_data(df, target_column=None)[0]  # Solo se necesitan las características para predicción

    # Realizar predicciones
    predictions = predict_with_models(models, X_new)

    # Guardar las predicciones
    save_predictions(predictions, output_file)
