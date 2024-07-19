import unittest
import pandas as pd
from models.model_utils import fetch_data_from_api, preprocess_data, calculate_metrics, calculate_classification_metrics, \
plot_feature_importance, plot_predictions
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier



class TestModelUtils(unittest.TestCase):
    def setUp(self):
        # Configuración inicial
        self.api_url = 'http://your-real-api-url'  # Reemplaza con la URL real de la API
        self.test_data_path = 'data/real_test_data.csv'  # Ruta a los datos de prueba reales
        self.target_column = 'target'
        self.model_params = {
            'n_estimators': 100,
            'max_depth': 10,
        }

    def test_fetch_data_from_api(self):
        """Prueba de obtención de datos desde la API real."""
        df = fetch_data_from_api(self.api_url)
        self.assertGreater(len(df), 0, "La longitud del DataFrame debe ser mayor a 0")
        self.assertIn('column_name', df.columns, "El DataFrame debe contener la columna 'column_name'")
        # Agregar más aserciones según las expectativas reales del DataFrame

    def test_preprocess_data(self):
        """Prueba de preprocesamiento de datos con datos reales."""
        df = pd.read_csv(self.test_data_path)
        X_train, X_test, y_train, y_test = preprocess_data(df, self.target_column)
        self.assertGreater(len(X_train), 0, "El conjunto de entrenamiento debe tener más de 0 filas")
        self.assertGreater(len(X_test), 0, "El conjunto de prueba debe tener más de 0 filas")
        self.assertEqual(len(X_train), len(y_train), "X_train y y_train deben tener la misma longitud")
        self.assertEqual(len(X_test), len(y_test), "X_test y y_test deben tener la misma longitud")

    def test_train_model(self):
        """Prueba de entrenamiento del modelo con parámetros reales."""
        df = pd.read_csv(self.test_data_path)
        X_train, X_test, y_train, y_test = preprocess_data(df, self.target_column)

        model = RandomForestRegressor(n_estimators=self.model_params['n_estimators'],
                                      max_depth=self.model_params['max_depth'])
        model.fit(X_train, y_train)
        self.assertIsNotNone(model, "El modelo entrenado no debe ser None")
        self.assertTrue(hasattr(model, 'predict'), "El modelo entrenado debe tener un método 'predict'")

        y_pred = model.predict(X_test)
        metrics = calculate_metrics(y_test, y_pred)
        self.assertGreater(metrics['R2'], 0.5, "El R2 del modelo debe ser mayor a 0.5")
        # Agrega rmás aserciones para validar el rendimiento del modelo

    def test_evaluate_classification_model(self):
        """Prueba de evaluación del modelo de clasificación con datos reales."""
        df = pd.read_csv(self.test_data_path)
        X_train, X_test, y_train, y_test = preprocess_data(df, self.target_column)

        model = RandomForestClassifier(n_estimators=self.model_params['n_estimators'],
                                       max_depth=self.model_params['max_depth'])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        metrics = calculate_classification_metrics(y_test, y_pred)
        self.assertGreater(metrics['Accuracy'], 0.5, "La precisión del modelo debe ser mayor a 0.5")
        self.assertIn('accuracy', metrics['Classification Report'],
                      "El informe de clasificación debe contener 'accuracy'")
        # Agregar más aserciones para validar la precisión del modelo

    def test_plot_feature_importance(self):
        """Prueba de la gráfica de importancia de características del modelo."""
        df = pd.read_csv(self.test_data_path)
        X_train, X_test, y_train, y_test = preprocess_data(df, self.target_column)

        model = RandomForestRegressor(n_estimators=self.model_params['n_estimators'],
                                      max_depth=self.model_params['max_depth'])
        model.fit(X_train, y_train)
        feature_names = X_train.columns
        plot_feature_importance(model, feature_names)
        # Verificar visualmente la gráfica generada

    def test_plot_predictions(self):
        """Prueba de la gráfica de predicciones del modelo."""
        df = pd.read_csv(self.test_data_path)
        X_train, X_test, y_train, y_test = preprocess_data(df, self.target_column)

        model = RandomForestRegressor(n_estimators=self.model_params['n_estimators'],
                                      max_depth=self.model_params['max_depth'])
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        plot_predictions(y_test, y_pred)
        # Verificar visualmente la gráfica generada


if __name__ == '__main__':
    unittest.main()
