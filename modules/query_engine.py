
import re
import pandas as pd


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """Convert text to lowercase and normalize spaces/symbols."""
    text = str(text).lower().strip()
    text = text.replace("_", " ")
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)
    return text


# ============================================================
# COLUMN DETECTION
# ============================================================

def get_numeric_columns(df):
    """Return numerical columns."""
    return df.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(df):
    """Return categorical/text columns."""
    return df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()


def find_column(df, query):
    """
    Find a column explicitly mentioned in the user's query.
    Uses normalized matching.
    """
    normalized_query = normalize_text(query)

    # Exact normalized column match
    for column in df.columns:
        normalized_column = normalize_text(column)

        if normalized_column in normalized_query:
            return column

    # Token-based matching
    best_column = None
    best_score = 0

    query_words = set(normalized_query.split())

    for column in df.columns:
        column_words = set(normalize_text(column).split())

        if not column_words:
            continue

        score = len(column_words.intersection(query_words))

        if score > best_score:
            best_score = score
            best_column = column

    return best_column if best_score > 0 else None


# ============================================================
# METRIC COLUMN DETECTION
# ============================================================

def find_metric_column(df, query):
    """
    Identify the numerical column that the user wants to analyze.
    Designed to work with different datasets.
    """

    numeric_columns = get_numeric_columns(df)

    if not numeric_columns:
        return None

    normalized_query = normalize_text(query)

    # --------------------------------------------------------
    # 1. Strong exact column matching
    # --------------------------------------------------------

    for column in numeric_columns:
        normalized_column = normalize_text(column)

        if normalized_column in normalized_query:
            return column

    # --------------------------------------------------------
    # 2. Semantic metric mappings
    # --------------------------------------------------------

    metric_keywords = {
        "purchase_amount": [
            "purchase amount",
            "purchase",
            "spending",
            "spend",
            "amount spent",
            "customer spending",
            "customer spend"
        ],

        "sales": [
            "sales",
            "sale"
        ],

        "revenue": [
            "revenue",
            "income"
        ],

        "profit": [
            "profit",
            "profits",
            "earnings"
        ],

        "salary": [
            "salary",
            "salaries",
            "pay",
            "income"
        ],

        "price": [
            "price",
            "cost",
            "amount"
        ],

        "rating": [
            "rating",
            "ratings",
            "score",
            "review"
        ],

        "age": [
            "age"
        ],

        "quantity": [
            "quantity",
            "qty",
            "units",
            "number of units"
        ],

        "count": [
            "count",
            "number",
            "records",
            "rows"
        ]
    }

    # --------------------------------------------------------
    # 3. Score each numerical column
    # --------------------------------------------------------

    best_column = None
    best_score = 0

    for column in numeric_columns:

        column_name = normalize_text(column)

        score = 0

        # Column words
        column_words = set(column_name.split())

        # Query words
        query_words = set(normalized_query.split())

        # Word overlap
        score += len(column_words.intersection(query_words)) * 5

        # ----------------------------------------------------
        # Purchase amount
        # ----------------------------------------------------

        if (
            "purchase" in normalized_query
            and "amount" in normalized_query
        ):
            if "purchase" in column_name and "amount" in column_name:
                score += 100

        elif "purchase" in normalized_query:
            if "purchase" in column_name:
                score += 80

        # ----------------------------------------------------
        # Spending
        # ----------------------------------------------------

        if any(word in normalized_query for word in ["spending", "spend"]):
            if any(word in column_name for word in ["purchase", "spending", "amount"]):
                score += 70

        # ----------------------------------------------------
        # Sales
        # ----------------------------------------------------

        if "sales" in normalized_query:
            if "sales" in column_name:
                score += 90

        # ----------------------------------------------------
        # Revenue
        # ----------------------------------------------------

        if "revenue" in normalized_query:
            if "revenue" in column_name:
                score += 90

        # ----------------------------------------------------
        # Profit
        # ----------------------------------------------------

        if "profit" in normalized_query:
            if "profit" in column_name:
                score += 90

        # ----------------------------------------------------
        # Salary
        # ----------------------------------------------------

        if "salary" in normalized_query:
            if "salary" in column_name:
                score += 90

        # ----------------------------------------------------
        # Rating
        # ----------------------------------------------------

        if any(word in normalized_query for word in ["rating", "score"]):
            if any(word in column_name for word in ["rating", "score"]):
                score += 90

        # ----------------------------------------------------
        # Age
        # ----------------------------------------------------

        if "age" in normalized_query:
            if "age" in column_name:
                score += 90

        # ----------------------------------------------------
        # Quantity
        # ----------------------------------------------------

        if any(word in normalized_query for word in ["quantity", "qty", "units"]):
            if any(word in column_name for word in ["quantity", "qty", "units"]):
                score += 90

        if score > best_score:
            best_score = score
            best_column = column

    # --------------------------------------------------------
    # 4. Fallback
    # --------------------------------------------------------

    if best_column is not None:
        return best_column

    # Avoid blindly choosing Age.
    # Prefer common business metrics.
    priority_words = [
        "amount",
        "sales",
        "revenue",
        "profit",
        "price",
        "cost",
        "quantity",
        "rating"
    ]

    for word in priority_words:
        for column in numeric_columns:
            if word in normalize_text(column):
                return column

    # Last fallback: first numerical column
    return numeric_columns[0]


# ============================================================
# GROUP COLUMN DETECTION
# ============================================================

def find_group_column(df, query):
    """
    Detect the categorical column used for grouping.

    Examples:
    average sales by gender
    total revenue by category
    count customers by location
    """

    normalized_query = normalize_text(query)

    categorical_columns = get_categorical_columns(df)

    if not categorical_columns:
        return None

    # --------------------------------------------------------
    # 1. Explicit column mentioned
    # --------------------------------------------------------

    for column in categorical_columns:
        normalized_column = normalize_text(column)

        if normalized_column in normalized_query:
            return column

    # --------------------------------------------------------
    # 2. Semantic mappings
    # --------------------------------------------------------

    semantic_groups = {
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
            "staff"
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
            "categories",
            "type",
            "types"
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
        ],

        "payment": [
            "payment",
            "payment method",
            "method"
        ],

        "shipping": [
            "shipping",
            "shipping type"
        ],

        "subscription": [
            "subscription",
            "subscription status"
        ]
    }

    # --------------------------------------------------------
    # 3. Score candidate columns
    # --------------------------------------------------------

    best_column = None
    best_score = 0

    for column in categorical_columns:

        column_name = normalize_text(column)

        for semantic_key, keywords in semantic_groups.items():

            if any(keyword in normalized_query for keyword in keywords):

                if semantic_key in column_name:
                    score = 100

                    if score > best_score:
                        best_score = score
                        best_column = column

                # Individual keyword matching
                for keyword in keywords:
                    if keyword in column_name and keyword in normalized_query:
                        score = 80

                        if score > best_score:
                            best_score = score
                            best_column = column

    return best_column


# ============================================================
# OPERATION DETECTION
# ============================================================

def detect_operation(query):
    """Detect what calculation the user wants."""

    query = normalize_text(query)

    # Average
    if any(word in query for word in [
        "average",
        "avg",
        "mean"
    ]):
        return "average"

    # Sum / total
    if any(word in query for word in [
        "total",
        "sum",
        "overall"
    ]):
        return "sum"

    # Maximum
    if any(word in query for word in [
        "maximum",
        "max",
        "highest",
        "largest",
        "greatest"
    ]):
        return "max"

    # Minimum
    if any(word in query for word in [
        "minimum",
        "min",
        "lowest",
        "smallest"
    ]):
        return "min"

    # Count
    if any(word in query for word in [
        "count",
        "how many",
        "number of"
    ]):
        return "count"

    return None


# ============================================================
# LIMIT DETECTION
# ============================================================

def detect_limit(query):
    """Detect top/bottom N."""

    query = normalize_text(query)

    match = re.search(
        r"(?:top|highest|bottom|lowest)\s+(\d+)",
        query
    )

    if match:
        return int(match.group(1))

    return None


def detect_limit_type(query):
    """Return top or bottom."""

    query = normalize_text(query)

    if any(word in query for word in [
        "top",
        "highest",
        "largest",
        "greatest"
    ]):
        return "top"

    if any(word in query for word in [
        "bottom",
        "lowest",
        "smallest"
    ]):
        return "bottom"

    return None


# ============================================================
# NUMBER DETECTION
# ============================================================

def find_number(query):
    """Find a number in the query."""

    match = re.search(r"\b(\d+)\b", str(query))

    if match:
        return int(match.group(1))

    return None


# ============================================================
# DATASET SUMMARY
# ============================================================

def dataset_summary(df):
    """Return a basic dataset summary."""

    rows = len(df)
    columns = len(df.columns)

    numeric_columns = get_numeric_columns(df)
    categorical_columns = get_categorical_columns(df)

    missing_values = int(df.isnull().sum().sum())

    return {
        "rows": rows,
        "columns": columns,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "missing_values": missing_values
    }


# ============================================================
# GROUPED OPERATIONS
# ============================================================

def grouped_average(df, group_column, metric_column):
    """Average metric by group."""

    result = (
        df.groupby(group_column, dropna=False)[metric_column]
        .mean()
        .reset_index()
    )

    result.columns = [
        group_column,
        f"Average {metric_column}"
    ]

    return result.sort_values(
        by=f"Average {metric_column}",
        ascending=False
    ).reset_index(drop=True)


def grouped_total(df, group_column, metric_column):
    """Total metric by group."""

    result = (
        df.groupby(group_column, dropna=False)[metric_column]
        .sum()
        .reset_index()
    )

    result.columns = [
        group_column,
        f"Total {metric_column}"
    ]

    return result.sort_values(
        by=f"Total {metric_column}",
        ascending=False
    ).reset_index(drop=True)


def grouped_count(df, group_column):
    """Count records by group."""

    result = (
        df.groupby(group_column, dropna=False)
        .size()
        .reset_index(name="Count")
    )

    return result.sort_values(
        by="Count",
        ascending=False
    ).reset_index(drop=True)


def grouped_max(df, group_column, metric_column):
    """Maximum metric by group."""

    result = (
        df.groupby(group_column, dropna=False)[metric_column]
        .max()
        .reset_index()
    )

    result.columns = [
        group_column,
        f"Maximum {metric_column}"
    ]

    return result.sort_values(
        by=f"Maximum {metric_column}",
        ascending=False
    ).reset_index(drop=True)


def grouped_min(df, group_column, metric_column):
    """Minimum metric by group."""

    result = (
        df.groupby(group_column, dropna=False)[metric_column]
        .min()
        .reset_index()
    )

    result.columns = [
        group_column,
        f"Minimum {metric_column}"
    ]

    return result.sort_values(
        by=f"Minimum {metric_column}",
        ascending=True
    ).reset_index(drop=True)


# ============================================================
# TOP / BOTTOM GROUPS
# ============================================================

def grouped_top_bottom(
    df,
    group_column,
    metric_column,
    limit,
    limit_type="top",
    operation="sum"
):
    """
    Return top/bottom groups.

    Examples:
    top 10 customers by spending
    top 5 products by sales
    bottom 3 departments by salary
    """

    if operation == "average":
        result = grouped_average(
            df,
            group_column,
            metric_column
        )

        value_column = f"Average {metric_column}"

    elif operation == "max":
        result = grouped_max(
            df,
            group_column,
            metric_column
        )

        value_column = f"Maximum {metric_column}"

    elif operation == "min":
        result = grouped_min(
            df,
            group_column,
            metric_column
        )

        value_column = f"Minimum {metric_column}"

    else:
        result = grouped_total(
            df,
            group_column,
            metric_column
        )

        value_column = f"Total {metric_column}"

    ascending = limit_type == "bottom"

    return (
        result.sort_values(
            by=value_column,
            ascending=ascending
        )
        .head(limit)
        .reset_index(drop=True)
    )


# ============================================================
# MAIN QUERY PROCESSOR
# ============================================================

def process_query(df, query):
    """
    Main natural-language query processor.

    Supports:
    - average
    - total
    - sum
    - maximum
    - minimum
    - count
    - group-by
    - top N
    - bottom N
    - dataset summary
    """

    if df is None or df.empty:
        return {
            "type": "error",
            "message": "The dataset is empty."
        }

    if query is None or not str(query).strip():
        return {
            "type": "error",
            "message": "Please enter a question."
        }

    normalized_query = normalize_text(query)

    # ========================================================
    # DATASET SUMMARY QUESTIONS
    # ========================================================

    if any(phrase in normalized_query for phrase in [
        "how many rows",
        "number of rows",
        "row count",
        "how many records",
        "number of records"
    ]):
        return {
            "type": "text",
            "message": f"The dataset contains {len(df):,} rows."
        }

    if any(phrase in normalized_query for phrase in [
        "how many columns",
        "number of columns",
        "column count"
    ]):
        return {
            "type": "text",
            "message": f"The dataset contains {len(df.columns):,} columns."
        }

    if any(phrase in normalized_query for phrase in [
        "dataset summary",
        "summarize dataset",
        "summary of dataset",
        "describe dataset"
    ]):
        summary = dataset_summary(df)

        return {
            "type": "summary",
            "data": summary
        }

    # ========================================================
    # DETECT OPERATION
    # ========================================================

    operation = detect_operation(normalized_query)

    # ========================================================
    # DETECT TOP / BOTTOM
    # ========================================================

    limit = detect_limit(normalized_query)
    limit_type = detect_limit_type(normalized_query)

    # ========================================================
    # DETECT GROUP ONLY WHEN QUERY EXPLICITLY ASKS FOR GROUPING
    # ========================================================

    group_column = None

    if (
        " by " in f" {normalized_query} "
        or "per " in normalized_query
        or "each " in normalized_query
    ):
        group_column = find_group_column(
            df,
            normalized_query
        )

    # ========================================================
    # COUNT QUESTIONS
    # ========================================================

    if operation == "count":

        # Grouped count
        if group_column is not None:

            result = grouped_count(
                df,
                group_column
            )

            if limit is not None and limit_type is not None:
                if limit_type == "top":
                    result = result.head(limit)
                else:
                    result = result.tail(limit)

                result = result.reset_index(drop=True)

            return {
                "type": "dataframe",
                "data": result
            }

        return {
            "type": "text",
            "message": f"The dataset contains {len(df):,} records."
        }

    # ========================================================
    # FIND METRIC
    # ========================================================

    metric_column = find_metric_column(
        df,
        normalized_query
    )

    if metric_column is None:
        return {
            "type": "error",
            "message": "I could not identify a numerical column for this question."
        }

    # Convert metric safely to numeric
    numeric_series = pd.to_numeric(
        df[metric_column],
        errors="coerce"
    )

    valid_values = numeric_series.dropna()

    if valid_values.empty:
        return {
            "type": "error",
            "message": f"The column '{metric_column}' does not contain usable numerical values."
        }

    # ========================================================
    # GROUPED QUESTIONS
    # ========================================================

    if group_column is not None:

        # Top / bottom grouped query
        if limit is not None and limit_type is not None:

            result = grouped_top_bottom(
                df.assign(**{metric_column: numeric_series}),
                group_column,
                metric_column,
                limit,
                limit_type,
                operation if operation in [
                    "average",
                    "max",
                    "min"
                ] else "sum"
            )

            return {
                "type": "dataframe",
                "data": result
            }

        # Average by group
        if operation == "average":

            result = grouped_average(
                df.assign(**{metric_column: numeric_series}),
                group_column,
                metric_column
            )

            return {
                "type": "dataframe",
                "data": result
            }

        # Total by group
        if operation == "sum":

            result = grouped_total(
                df.assign(**{metric_column: numeric_series}),
                group_column,
                metric_column
            )

            return {
                "type": "dataframe",
                "data": result
            }

        # Maximum by group
        if operation == "max":

            result = grouped_max(
                df.assign(**{metric_column: numeric_series}),
                group_column,
                metric_column
            )

            return {
                "type": "dataframe",
                "data": result
            }

        # Minimum by group
        if operation == "min":

            result = grouped_min(
                df.assign(**{metric_column: numeric_series}),
                group_column,
                metric_column
            )

            return {
                "type": "dataframe",
                "data": result
            }

    # ========================================================
    # TOP / BOTTOM WITHOUT GROUPING
    # ========================================================

    if limit is not None and limit_type is not None:

        result = pd.DataFrame({
            metric_column: valid_values
        })

        ascending = limit_type == "bottom"

        result = (
            result.sort_values(
                by=metric_column,
                ascending=ascending
            )
            .head(limit)
            .reset_index(drop=True)
        )

        return {
            "type": "dataframe",
            "data": result
        }

    # ========================================================
    # SIMPLE AVERAGE
    # ========================================================

    if operation == "average":

        value = valid_values.mean()

        return {
            "type": "text",
            "message": (
                f"The average of '{metric_column}' is "
                f"{value:,.2f}."
            )
        }

    # ========================================================
    # SIMPLE SUM
    # ========================================================

    if operation == "sum":

        value = valid_values.sum()

        return {
            "type": "text",
            "message": (
                f"The total of '{metric_column}' is "
                f"{value:,.2f}."
            )
        }

    # ========================================================
    # SIMPLE MAXIMUM
    # ========================================================

    if operation == "max":

        value = valid_values.max()

        return {
            "type": "text",
            "message": (
                f"The maximum of '{metric_column}' is "
                f"{value:,.2f}."
            )
        }

    # ========================================================
    # SIMPLE MINIMUM
    # ========================================================

    if operation == "min":

        value = valid_values.min()

        return {
            "type": "text",
            "message": (
                f"The minimum of '{metric_column}' is "
                f"{value:,.2f}."
            )
        }

    # ========================================================
    # SHOW NUMERICAL COLUMN
    # ========================================================

    if metric_column is not None:

        return {
            "type": "dataframe",
            "data": df[[metric_column]].head(10)
        }

    # ========================================================
    # FALLBACK
    # ========================================================

    return {
        "type": "error",
        "message": (
            "I could not understand the question. "
            "Try asking something like: "
            "'What is the average sales?', "
            "'What is the total revenue?', or "
            "'What is the average sales by category?'"
        )
    }
