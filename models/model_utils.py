import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import requests


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


def preprocess_data(data, target_column, test_size=0.2, random_state=42):
    """
    Preprocesa los datos dividiéndolos en características y etiquetas, y luego en conjuntos de entrenamiento y prueba.

    :param data: DataFrame con los datos
    :param target_column: Nombre de la columna objetivo
    :param test_size: Proporción del conjunto de prueba
    :param random_state: Estado aleatorio para la división de datos
    :return: Conjuntos de entrenamiento y prueba para características y etiquetas
    """
    data = data.drop_duplicates()
    data = data.dropna()
    categorical_columns = data.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 0:
        data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
    numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
    scaler = MinMaxScaler()
    data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

    X = data.drop(columns=[target_column])
    y = data[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    return X_train, X_test, y_train, y_test


def calculate_metrics(y_true, y_pred):
    """
    Calcula métricas de evaluación para un modelo de regresión.

    :param y_true: Valores verdaderos
    :param y_pred: Predicciones del modelo
    :return: Diccionario con métricas de evaluación
    """
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)

    return {
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    }


def calculate_classification_metrics(y_true, y_pred):
    """
    Calcula métricas de evaluación para un modelo de clasificación.

    :param y_true: Valores verdaderos
    :param y_pred: Predicciones del modelo
    :return: Diccionario con métricas de evaluación
    """
    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, output_dict=True)

    return {
        "Accuracy": accuracy,
        "Classification Report": report
    }


def plot_feature_importance(model, feature_names):
    """
    Grafica la importancia de las características de un modelo.

    :param model: Modelo entrenado
    :param feature_names: Lista de nombres de características
    """
    importance = model.feature_importances_
    indices = np.argsort(importance)

    plt.figure(figsize=(10, 6))
    plt.title('Importancia de las Características')
    plt.barh(range(len(indices)), importance[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
    plt.xlabel('Importancia Relativa')
    plt.show()


def plot_predictions(y_true, y_pred):
    """
    Grafica las predicciones del modelo frente a los valores verdaderos.

    :param y_true: Valores verdaderos
    :param y_pred: Predicciones del modelo
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_true, y_pred, edgecolor='k', s=50)
    plt.xlabel('Valores Verdaderos')
    plt.ylabel('Predicciones')
    plt.title('Valores Verdaderos vs Predicciones')
    plt.show()
