from sklearn.model_selection import train_test_split
from data_loader import DataLoader

class DataSplitter:
    def __init__(self, api_url, target_column, test_size=0.2, random_state=42):
        """
        Initialize the DataSplitter with the data from the API and parameters for splitting.

        :param api_url: URL of the Django API endpoint to fetch data
        :param target_column: Name of the target column for supervised learning
        :param test_size: Proportion of the dataset to include in the test split
        :param random_state: Seed used by the random number generator
        """
        self.api_url = api_url
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.data_loader = DataLoader(api_url)
        self.data = self.load_data()

    def load_data(self):
        """
        Load the data from the Django API using the DataLoader class.

        :return: DataFrame with the dataset
        """
        print("Fetching data from API...")
        data = self.data_loader.get_data()
        print(f"Data fetched with {len(data)} records")
        return data

    def split_data(self):
        """
        Split the data into training and testing sets.

        :return: Tuple of DataFrames (X_train, X_test, y_train, y_test)
        """
        X = self.data.drop(self.target_column, axis=1)
        y = self.data[self.target_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        print(f"Data split into training and testing sets with test size = {self.test_size}")
        return X_train, X_test, y_train, y_test

    def save_split_data(self, X_train, X_test, y_train, y_test, output_dir):
        """
        Save the split data into CSV files.

        :param X_train: Training features
        :param X_test: Testing features
        :param y_train: Training labels
        :param y_test: Testing labels
        :param output_dir: Directory to save the split data
        """
        X_train.to_csv(f'{output_dir}/X_train.csv', index=False)
        X_test.to_csv(f'{output_dir}/X_test.csv', index=False)
        y_train.to_csv(f'{output_dir}/y_train.csv', index=False)
        y_test.to_csv(f'{output_dir}/y_test.csv', index=False)
        print(f"Split data saved to {output_dir}")

# Example usage
if __name__ == "__main__":
    # Replace with the actual API endpoint and target column
    api_url = 'http://<django-backend-url>/api/data_endpoint/'
    target_column = 'target_column'  # Replace with actual target column name

    # Initialize DataSplitter
    splitter = DataSplitter(api_url, target_column)

    # Split the data
    X_train, X_test, y_train, y_test = splitter.split_data()

    # Save the split data
    output_dir = 'path/to/save/split/data'
    splitter.save_split_data(X_train, X_test, y_train, y_test, output_dir)
