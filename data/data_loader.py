import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

class DataLoader:
    def __init__(self, api_url, target_column, test_size=0.2, random_state=42):
        self.api_url = api_url
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.data = self.load_data()
        self.cleaned_data = self.preprocess_data(self.data)

    def load_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data)
            print(f"Data loaded successfully from {self.api_url}")
            return df
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching data from API: {e}")

    def preprocess_data(self, data):
        data = data.drop_duplicates()
        data = data.dropna()
        categorical_columns = data.select_dtypes(include=['object']).columns
        if len(categorical_columns) > 0:
            data = pd.get_dummies(data, columns=categorical_columns, drop_first=True)
        numerical_columns = data.select_dtypes(include=['int64', 'float64']).columns
        scaler = MinMaxScaler()
        data[numerical_columns] = scaler.fit_transform(data[numerical_columns])
        if self.target_column not in data.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in the data.")
        return data

    def get_data(self):
        return self.cleaned_data

    def split_data(self):
        X = self.cleaned_data.drop(self.target_column, axis=1)
        y = self.cleaned_data[self.target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        print(f"Data split into training and testing sets with test size = {self.test_size}")
        return X_train, X_test, y_train, y_test
