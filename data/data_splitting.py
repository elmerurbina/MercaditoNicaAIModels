import pandas as pd
from sklearn.model_selection import train_test_split
import pymysql

class DataSplitter:
    def __init__(self, db_url, table_name, target_column, test_size=0.2, random_state=42):
        """
        Initialize the DataSplitter with the data from the database and parameters for splitting.

        :param db_url: Database URL
        :param table_name: Name of the table to fetch data from
        :param target_column: Name of the target column for supervised learning
        :param test_size: Proportion of the dataset to include in the test split
        :param random_state: Seed used by the random number generator
        """
        self.db_url = db_url
        self.table_name = table_name
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.connection = self.create_connection()
        self.data = self.load_data()

    def create_connection(self):
        """
        Create a connection to the database.

        :return: Database connection object
        """
        # Example for PyMySQL; adjust parameters as needed
        connection = pymysql.connect(
            host='sql111.byetcluster.com',
            user='your_username',
            password='your_password',
            database='ezyro_36944054_MercaditoNica'
        )
        return connection

    def load_data(self):
        """
        Load the data from the SQL database.

        :return: DataFrame with the dataset
        """
        print("Connecting to database...")
        query = f"SELECT * FROM {self.table_name}"
        data = pd.read_sql(query, self.connection)
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

    def save_split_data_to_db(self, X_train, X_test, y_train, y_test):
        """
        Save the split data into the database.

        :param X_train: Training features
        :param X_test: Testing features
        :param y_train: Training labels
        :param y_test: Testing labels
        """
        with self.connection.cursor() as cursor:
            # Save training data
            train_data = X_train.copy()
            train_data[self.target_column] = y_train.values
            train_data.to_sql('model_training_data_split', con=self.connection, if_exists='replace', index=False)
            print("Training data saved to 'model_training_data_split' table")

            # Save testing data
            test_data = X_test.copy()
            test_data[self.target_column] = y_test.values
            test_data.to_sql('model_testing_data_split', con=self.connection, if_exists='replace', index=False)
            print("Testing data saved to 'model_testing_data_split' table")

    def fetch_data_from_db(self, table_name):
        """
        Fetch data from a specified table in the database.

        :param table_name: Name of the table to fetch data from
        :return: DataFrame with the dataset
        """
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, self.connection)
        print(f"Data fetched from '{table_name}' with {len(data)} records")
        return data

# Example usage
if __name__ == "__main__":
    # Replace with the actual database URL and table name
    db_url = 'mysql+pymysql://username:password@sql111.byetcluster.com/ezyro_36944054_MercaditoNica'
    table_name = 'model_training_data'
    target_column = 'target_data'

    # Initialize DataSplitter
    splitter = DataSplitter(db_url, table_name, target_column)

    # Split the data
    X_train, X_test, y_train, y_test = splitter.split_data()

    # Save the split data to the database
    splitter.save_split_data_to_db(X_train, X_test, y_train, y_test)

    # Optionally, fetch data from another table
    fetched_data = splitter.fetch_data_from_db('model_training_data_split')
