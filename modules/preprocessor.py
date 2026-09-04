import pandas as pd


def clean_column_names(df):
    """
    Clean column names by removing extra spaces
    and replacing spaces with underscores.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace(" ", "_")
    )

    return df


def remove_duplicates(df):
    """
    Remove duplicate rows from the dataset.
    """

    df = df.copy()

    duplicates_removed = df.duplicated().sum()

    df = df.drop_duplicates()

    return df, duplicates_removed


def handle_missing_values(df):
    """
    Handle missing values.

    Numerical columns:
        Missing values are replaced with the median.

    Categorical columns:
        Missing values are replaced with the mode.
    """

    df = df.copy()

    missing_before = df.isnull().sum().sum()

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    # Fill numerical missing values with median
    for column in numerical_columns:

        if df[column].isnull().any():

            median_value = df[column].median()

            df[column] = df[column].fillna(median_value)

    # Fill categorical missing values with mode
    for column in categorical_columns:

        if df[column].isnull().any():

            mode_values = df[column].mode()

            if not mode_values.empty:

                df[column] = df[column].fillna(
                    mode_values.iloc[0]
                )

    missing_after = df.isnull().sum().sum()

    return df, missing_before, missing_after


def preprocess_dataset(df):
    """
    Perform the complete preprocessing pipeline.
    """

    # Keep original dataset unchanged
    processed_df = df.copy()

    # Step 1: Clean column names
    processed_df = clean_column_names(
        processed_df
    )

    # Step 2: Remove duplicate rows
    processed_df, duplicates_removed = remove_duplicates(
        processed_df
    )

    # Step 3: Handle missing values
    (
        processed_df,
        missing_before,
        missing_after
    ) = handle_missing_values(
        processed_df
    )

    preprocessing_info = {
        "original_rows": df.shape[0],
        "original_columns": df.shape[1],
        "processed_rows": processed_df.shape[0],
        "processed_columns": processed_df.shape[1],
        "duplicates_removed": duplicates_removed,
        "missing_values_before": missing_before,
        "missing_values_after": missing_after
    }

    return processed_df, preprocessing_info