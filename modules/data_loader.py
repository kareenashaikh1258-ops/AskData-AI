import pandas as pd


def load_dataset(uploaded_file):
    """
    Load a CSV or Excel file into a Pandas DataFrame.
    """

    if uploaded_file is None:
        return None, "No file uploaded."

    file_name = uploaded_file.name.lower()

    try:

        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        else:
            return None, "Unsupported file type. Please upload a CSV or XLSX file."

        if df.empty:
            return None, "The uploaded dataset is empty."

        # Remove extra spaces from column names
        df.columns = df.columns.astype(str).str.strip()

        return df, None

    except Exception as e:
        return None, f"Error loading dataset: {str(e)}"