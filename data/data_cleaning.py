import pandas as pd


def handle_missing_values(df):
    """
    Handle missing values in the DataFrame.

    :param df: DataFrame with potential missing values
    :return: DataFrame with missing values handled
    """
    # Example: Fill missing numerical values with the mean and categorical values with the mode
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        df[column].fillna(df[column].mean(), inplace=True)
    for column in df.select_dtypes(include=['object']).columns:
        df[column].fillna(df[column].mode()[0], inplace=True)
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.

    :param df: DataFrame with potential duplicate rows
    :return: DataFrame with duplicates removed
    """
    return df.drop_duplicates()


def convert_data_types(df):
    """
    Convert data types of the DataFrame columns as needed.

    :param df: DataFrame with columns to convert
    :return: DataFrame with columns converted to appropriate data types
    """
    df['date'] = pd.to_datetime(df['date'])
    df['hour'] = pd.to_datetime(df['hour']).dt.hour
    df['sell_price'] = df['sell_price'].astype(float)
    df['material_cost_per_unit'] = df['material_cost_per_unit'].astype(float)
    df['quantity_per_unit'] = df['quantity_per_unit'].astype(int)
    df['price_per_unit'] = df['price_per_unit'].astype(float)
    df['transport_cost'] = df['transport_cost'].astype(float)
    df['labor_cost'] = df['labor_cost'].astype(float)
    df['material_costs'] = df['material_costs'].astype(float)
    df['other_expenses'] = df['other_expenses'].astype(float)
    return df


def clean_data(df):
    """
    Perform all data cleaning steps on the DataFrame.

    :param df: Raw DataFrame
    :return: Cleaned DataFrame
    """
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = convert_data_types(df)
    return df
