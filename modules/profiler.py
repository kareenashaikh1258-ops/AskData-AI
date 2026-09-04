import pandas as pd


def get_basic_info(df):
    """
    Return basic information about the dataset.
    """

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns)
    }


def get_data_types(df):
    """
    Return the data type of every column.
    """

    return df.dtypes.astype(str).to_dict()


def get_missing_values(df):
    """
    Return missing-value count for every column.
    """

    return df.isnull().sum().to_dict()


def get_unique_values(df):
    """
    Return the number of unique values for every column.
    """

    return df.nunique().to_dict()


def get_numerical_columns(df):
    """
    Identify numerical columns.
    """

    return df.select_dtypes(
        include=["number"]
    ).columns.tolist()


def get_categorical_columns(df):
    """
    Identify categorical/text columns.
    """

    return df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


def get_statistics(df):
    """
    Return descriptive statistics for numerical columns.
    """

    return df.describe().T


def profile_dataset(df):
    """
    Generate a complete dataset profile.
    """

    profile = {
        "basic_info": get_basic_info(df),
        "data_types": get_data_types(df),
        "missing_values": get_missing_values(df),
        "unique_values": get_unique_values(df),
        "numerical_columns": get_numerical_columns(df),
        "categorical_columns": get_categorical_columns(df),
        "statistics": get_statistics(df)
    }

    return profile