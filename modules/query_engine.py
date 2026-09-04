import pandas as pd
import re


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Normalize text so that different forms of column names
    and user questions can be compared.
    """

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# GET NUMERICAL COLUMNS
# ============================================================

def get_numeric_columns(df):

    return df.select_dtypes(
        include="number"
    ).columns.tolist()


# ============================================================
# GET CATEGORICAL COLUMNS
# ============================================================

def get_categorical_columns(df):

    return df.select_dtypes(
        exclude="number"
    ).columns.tolist()


# ============================================================
# FIND COLUMN FROM USER QUESTION
# ============================================================

def find_column(df, query):

    normalized_query = normalize_text(query)

    columns = df.columns.tolist()

    # --------------------------------------------------------
    # Exact column matching
    # --------------------------------------------------------

    for column in sorted(
        columns,
        key=lambda x: len(normalize_text(x)),
        reverse=True
    ):

        normalized_column = normalize_text(column)

        if normalized_column in normalized_query:

            return column

    return None


# ============================================================
# FIND GROUP COLUMN
# ============================================================

def find_group_column(df, query):

    # First try exact column name
    exact_column = find_column(df, query)

    if exact_column is not None:

        return exact_column

    normalized_query = normalize_text(query)

    query_words = set(
        normalized_query.split()
    )

    # --------------------------------------------------------
    # Generic semantic mappings
    # --------------------------------------------------------

    mappings = {

        "customer": [
            "customer",
            "customers",
            "client",
            "clients",
            "buyer",
            "buyers"
        ],

        "user": [
            "user",
            "users"
        ],

        "employee": [
            "employee",
            "employees",
            "staff",
            "worker",
            "workers"
        ],

        "department": [
            "department",
            "departments",
            "dept"
        ],

        "product": [
            "product",
            "products",
            "item",
            "items"
        ],

        "category": [
            "category",
            "categories"
        ],

        "city": [
            "city",
            "cities"
        ],

        "state": [
            "state",
            "states"
        ],

        "country": [
            "country",
            "countries"
        ],

        "region": [
            "region",
            "regions"
        ],

        "location": [
            "location",
            "locations",
            "place",
            "places"
        ],

        "gender": [
            "gender",
            "sex"
        ],

        "season": [
            "season",
            "seasons"
        ]
    }

    # --------------------------------------------------------
    # Search semantic matches
    # --------------------------------------------------------

    for semantic, keywords in mappings.items():

        if not any(
            keyword in query_words
            for keyword in keywords
        ):
            continue

        best_column = None
        best_score = 0

        for column in df.columns:

            column_text = normalize_text(column)

            column_words = set(
                column_text.split()
            )

            score = 0

            for keyword in keywords:

                if keyword in column_words:

                    score += 3

                elif keyword in column_text:

                    score += 1

            # Strong ID matching
            if semantic == "customer":

                if (
                    "customer" in column_text
                    and "id" in column_text
                ):

                    score += 10

            if semantic == "user":

                if (
                    "user" in column_text
                    and "id" in column_text
                ):

                    score += 10

            if score > best_score:

                best_score = score
                best_column = column

        if best_column is not None:

            return best_column

    return None


# ============================================================
# FIND NUMERICAL METRIC
# ============================================================

def find_metric_column(df, query):

    numeric_columns = get_numeric_columns(df)

    if not numeric_columns:

        return None

    # --------------------------------------------------------
    # Exact column matching
    # --------------------------------------------------------

    normalized_query = normalize_text(query)

    for column in sorted(
        numeric_columns,
        key=lambda x: len(normalize_text(x)),
        reverse=True
    ):

        normalized_column = normalize_text(column)

        if normalized_column in normalized_query:

            return column

    # --------------------------------------------------------
    # Semantic metric mapping
    # --------------------------------------------------------

    mappings = {

        "spending": [
            "spending",
            "spend",
            "spent",
            "purchase",
            "purchases",
            "amount",
            "buying"
        ],

        "sales": [
            "sales",
            "sale"
        ],

        "revenue": [
            "revenue",
            "income",
            "earning",
            "earnings"
        ],

        "profit": [
            "profit",
            "profits"
        ],

        "salary": [
            "salary",
            "salaries",
            "pay",
            "wage",
            "wages"
        ],

        "price": [
            "price",
            "prices",
            "cost",
            "costs"
        ],

        "rating": [
            "rating",
            "ratings",
            "score",
            "scores"
        ],

        "age": [
            "age",
            "ages"
        ],

        "quantity": [
            "quantity",
            "quantities",
            "units"
        ]
    }

    query_words = set(
        normalized_query.split()
    )

    # --------------------------------------------------------
    # Search each semantic group
    # --------------------------------------------------------

    for semantic, keywords in mappings.items():

        if not any(
            keyword in query_words
            for keyword in keywords
        ):
            continue

        best_column = None
        best_score = 0

        for column in numeric_columns:

            column_text = normalize_text(column)

            column_words = set(
                column_text.split()
            )

            score = 0

            for keyword in keywords:

                if keyword in column_words:

                    score += 3

                elif keyword in column_text:

                    score += 1

            # Special case:
            # spending -> purchase amount

            if semantic == "spending":

                if (
                    "purchase" in column_words
                    and "amount" in column_words
                ):

                    score += 15

            # sales -> sales column

            if semantic == "sales":

                if "sales" in column_words:

                    score += 15

            # revenue -> revenue column

            if semantic == "revenue":

                if "revenue" in column_words:

                    score += 15

            # profit -> profit column

            if semantic == "profit":

                if "profit" in column_words:

                    score += 15

            # salary -> salary column

            if semantic == "salary":

                if "salary" in column_words:

                    score += 15

            # rating -> rating column

            if semantic == "rating":

                if "rating" in column_words:

                    score += 15

            if score > best_score:

                best_score = score
                best_column = column

        if best_column is not None:

            return best_column

    # --------------------------------------------------------
    # If there is only one numerical column
    # --------------------------------------------------------

    if len(numeric_columns) == 1:

        return numeric_columns[0]

    return None


# ============================================================
# DETECT OPERATION
# ============================================================

def detect_operation(query):

    query = normalize_text(query)

    words = query.split()

    # Average
    if any(
        word in words
        for word in [
            "average",
            "avg",
            "mean"
        ]
    ):

        return "mean"

    # Sum
    if any(
        word in words
        for word in [
            "total",
            "sum",
            "overall"
        ]
    ):

        return "sum"

    # Maximum
    if any(
        word in words
        for word in [
            "highest",
            "maximum",
            "max",
            "largest"
        ]
    ):

        return "max"

    # Minimum
    if any(
        word in words
        for word in [
            "lowest",
            "minimum",
            "min",
            "smallest"
        ]
    ):

        return "min"

    # Count
    if (
        "count" in words
        or "number" in words
        or "how many" in query
    ):

        return "count"

    return None


# ============================================================
# DETECT TOP / BOTTOM
# ============================================================

def detect_limit_type(query):

    query = normalize_text(query)

    if "top" in query:

        return "top"

    if "highest" in query:

        return "top"

    if "bottom" in query:

        return "bottom"

    if "lowest" in query:

        return "bottom"

    return None


# ============================================================
# FIND NUMBER
# ============================================================

def find_number(query, default=10):

    numbers = re.findall(
        r"\b\d+\b",
        str(query)
    )

    if numbers:

        return int(numbers[0])

    return default


# ============================================================
# DATASET SUMMARY
# ============================================================

def dataset_summary(df):

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "column_names":
            df.columns.tolist(),

        "numerical_columns":
            get_numeric_columns(df),

        "categorical_columns":
            get_categorical_columns(df)
    }


# ============================================================
# TOP / BOTTOM GROUPED ANALYSIS
# ============================================================

def grouped_top_bottom(
    df,
    group_column,
    metric_column,
    limit,
    direction
):

    grouped = (
        df.groupby(
            group_column,
            dropna=False
        )[metric_column]
        .sum()
        .reset_index()
    )

    if direction == "top":

        grouped = grouped.sort_values(
            by=metric_column,
            ascending=False
        )

    else:

        grouped = grouped.sort_values(
            by=metric_column,
            ascending=True
        )

    return grouped.head(
        limit
    ).reset_index(drop=True)


# ============================================================
# GROUPED AVERAGE
# ============================================================
def grouped_average(df, group_column, metric_column):

    result = (
        df.groupby(
            group_column,
            dropna=False,
            as_index=False
        )[metric_column]
        .mean()
    )

    result = result.rename(
        columns={
            metric_column: f"Average {metric_column}"
        }
    )

    return result


# ============================================================
# GROUPED TOTAL
# ============================================================

def grouped_total(df, group_column, metric_column):

    result = (
        df.groupby(
            group_column,
            dropna=False,
            as_index=False
        )[metric_column]
        .sum()
    )

    result = result.rename(
        columns={
            metric_column: f"Total {metric_column}"
        }
    )

    return result
# ============================================================
# GROUPED COUNT
# ============================================================

def grouped_count(
    df,
    group_column
):

    return (
        df.groupby(
            group_column,
            dropna=False
        )
        .size()
        .reset_index(
            name="Count"
        )
    )


# ============================================================
# PROCESS QUERY
# ============================================================

def process_query(df, query):

    if df is None:

        return {
            "type": "error",
            "result":
                "Please upload a dataset first."
        }

    if df.empty:

        return {
            "type": "error",
            "result":
                "The uploaded dataset is empty."
        }

    query = str(query).strip()

    if not query:

        return {
            "type": "error",
            "result":
                "Please enter a question."
        }

    normalized_query = normalize_text(query)

    # ========================================================
    # DATASET SUMMARY
    # ========================================================

    if any(
        phrase in normalized_query
        for phrase in [
            "dataset summary",
            "describe dataset",
            "dataset information",
            "dataset info",
            "about dataset"
        ]
    ):

        return {
            "type": "summary",
            "result":
                dataset_summary(df)
        }

    # ========================================================
    # ROW COUNT
    # ========================================================

    if (
        "how many rows" in normalized_query
        or "number of rows" in normalized_query
        or "total rows" in normalized_query
    ):

        return {
            "type": "text",
            "result":
                f"The dataset contains {len(df)} rows."
        }

    # ========================================================
    # COLUMN COUNT
    # ========================================================

    if (
        "how many columns" in normalized_query
        or "number of columns" in normalized_query
        or "total columns" in normalized_query
    ):

        return {
            "type": "text",
            "result":
                f"The dataset contains {len(df.columns)} columns."
        }

    # ========================================================
    # COLUMN NAMES
    # ========================================================

    if any(
        phrase in normalized_query
        for phrase in [
            "column names",
            "list columns",
            "what columns"
        ]
    ):

        return {
            "type": "dataframe",
            "result":
                pd.DataFrame(
                    {
                        "Column Name":
                            df.columns.tolist()
                    }
                )
        }

    # ========================================================
    # UNIQUE VALUES
    # ========================================================

    if "unique values" in normalized_query:

        column = find_column(
            df,
            query
        )

        if column is None:

            column = find_group_column(
                df,
                query
            )

        if column:

            values = (
                df[column]
                .dropna()
                .unique()
                .tolist()
            )

            return {
                "type": "dataframe",
                "result":
                    pd.DataFrame(
                        {
                            column:
                                values
                        }
                    )
            }

        return {
            "type": "error",
            "result":
                "I could not identify which column you want unique values for."
        }

    # ========================================================
    # FIND GROUP / METRIC / OPERATION
    # ========================================================

    group_column = find_group_column(
        df,
        query
    )

    metric_column = find_metric_column(
        df,
        query
    )

    operation = detect_operation(
        query
    )

    limit_type = detect_limit_type(
        query
    )

    limit = find_number(
        query,
        default=10
    )

    # ========================================================
    # TOP / BOTTOM ANALYSIS
    # ========================================================

    if (
        group_column is not None
        and metric_column is not None
        and limit_type is not None
    ):

        result = grouped_top_bottom(
            df,
            group_column,
            metric_column,
            limit,
            limit_type
        )

        return {
            "type": "dataframe",
            "result": result
        }

    # ========================================================
    # GROUPED AVERAGE
    # ========================================================

    if (
        group_column is not None
        and metric_column is not None
        and operation == "mean"
    ):

        result = grouped_average(
            df,
            group_column,
            metric_column
        )

        return {
            "type": "dataframe",
            "result": result
        }

    # ========================================================
    # GROUPED TOTAL
    # ========================================================

    if (
        group_column is not None
        and metric_column is not None
        and operation == "sum"
    ):

        result = grouped_total(
            df,
            group_column,
            metric_column
        )

        return {
            "type": "dataframe",
            "result": result
        }

    # ========================================================
    # GROUPED COUNT
    # ========================================================

    if (
        group_column is not None
        and operation == "count"
    ):

        result = grouped_count(
            df,
            group_column
        )

        return {
            "type": "dataframe",
            "result": result
        }

    # ========================================================
    # SIMPLE AVERAGE
    # ========================================================

    if (
        metric_column is not None
        and operation == "mean"
    ):

        value = df[
            metric_column
        ].mean()

        return {
            "type": "text",
            "result":
                f"The average of '{metric_column}' is {value:.2f}."
        }

    # ========================================================
    # SIMPLE TOTAL
    # ========================================================

    if (
        metric_column is not None
        and operation == "sum"
    ):

        value = df[
            metric_column
        ].sum()

        return {
            "type": "text",
            "result":
                f"The total of '{metric_column}' is {value:.2f}."
        }

    # ========================================================
    # SIMPLE MAXIMUM
    # ========================================================

    if (
        metric_column is not None
        and operation == "max"
    ):

        value = df[
            metric_column
        ].max()

        return {
            "type": "text",
            "result":
                f"The highest value of '{metric_column}' is {value}."
        }

    # ========================================================
    # SIMPLE MINIMUM
    # ========================================================

    if (
        metric_column is not None
        and operation == "min"
    ):

        value = df[
            metric_column
        ].min()

        return {
            "type": "text",
            "result":
                f"The lowest value of '{metric_column}' is {value}."
        }

    # ========================================================
    # TOP RECORDS
    # ========================================================

    if (
        "top records" in normalized_query
        or "top rows" in normalized_query
    ):

        return {
            "type": "dataframe",
            "result":
                df.head(limit)
        }

    # ========================================================
    # BOTTOM RECORDS
    # ========================================================

    if (
        "bottom records" in normalized_query
        or "bottom rows" in normalized_query
    ):

        return {
            "type": "dataframe",
            "result":
                df.tail(limit)
        }

    # ========================================================
    # FALLBACK
    # ========================================================

    return {
        "type": "error",
        "result":
            "I could not understand this question yet. "
            "Try asking about rows, columns, average, "
            "total, highest, lowest, unique values, "
            "top records, bottom records, counts, "
            "or grouped analysis."
    }