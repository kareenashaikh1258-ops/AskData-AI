
import pandas as pd
import streamlit as st

from modules.data_loader import load_dataset
from modules.profiler import profile_dataset
from modules.preprocessor import preprocess_dataset
from modules.query_engine import process_query


# ===================================================
# PAGE CONFIGURATION
# ===================================================

st.set_page_config(
    page_title="AskData AI",
    page_icon="📊",
    layout="wide"
)


# ===================================================
# APPLICATION HEADER
# ===================================================

st.title("📊 AskData AI")

st.subheader("Intelligent Data Analyst Assistant")

st.write(
    "Upload your dataset and ask questions using natural language."
)


# ===================================================
# DATASET UPLOAD
# ===================================================

uploaded_file = st.file_uploader(
    "📂 Upload your dataset",
    type=["csv", "xlsx"]
)


# ===================================================
# PROCESS UPLOADED DATASET
# ===================================================

if uploaded_file is not None:

    # ------------------------------------------------
    # LOAD DATASET
    # ------------------------------------------------

    df, error = load_dataset(uploaded_file)


    # ------------------------------------------------
    # ERROR HANDLING
    # ------------------------------------------------

    if error:

        st.error(error)


    else:

        st.success("✅ Dataset uploaded successfully!")


        # =================================================
        # DATASET PREVIEW
        # =================================================

        st.divider()

        st.subheader("📄 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        st.write(
            f"**Rows:** {df.shape[0]}  |  "
            f"**Columns:** {df.shape[1]}"
        )


        # =================================================
        # DATASET PROFILING
        # =================================================

        st.divider()

        st.subheader("📋 Dataset Profile")

        profile = profile_dataset(df)

        basic_info = profile["basic_info"]


        # =================================================
        # ROWS AND COLUMNS
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Number of Rows",
                basic_info["rows"]
            )

        with col2:

            st.metric(
                "Number of Columns",
                basic_info["columns"]
            )


        # =================================================
        # COLUMN DATA TYPES
        # =================================================

        st.write("### 🔤 Column Data Types")

        data_types_df = pd.DataFrame(
            list(profile["data_types"].items()),
            columns=["Column", "Data Type"]
        )

        st.dataframe(
            data_types_df,
            use_container_width=True
        )


        # =================================================
        # MISSING VALUES
        # =================================================

        st.write("### ⚠️ Missing Values")

        missing_df = pd.DataFrame(
            list(profile["missing_values"].items()),
            columns=["Column", "Missing Values"]
        )

        st.dataframe(
            missing_df,
            use_container_width=True
        )


        # =================================================
        # UNIQUE VALUES
        # =================================================

        st.write("### 🔢 Unique Values")

        unique_df = pd.DataFrame(
            list(profile["unique_values"].items()),
            columns=["Column", "Unique Values"]
        )

        st.dataframe(
            unique_df,
            use_container_width=True
        )


        # =================================================
        # NUMERICAL COLUMNS
        # =================================================

        st.write("### 🔢 Numerical Columns")

        numerical_columns = profile["numerical_columns"]

        if numerical_columns:

            st.write(numerical_columns)

        else:

            st.info("No numerical columns found.")


        # =================================================
        # CATEGORICAL COLUMNS
        # =================================================

        st.write("### 🏷️ Categorical Columns")

        categorical_columns = profile["categorical_columns"]

        if categorical_columns:

            st.write(categorical_columns)

        else:

            st.info("No categorical columns found.")


        # =================================================
        # DESCRIPTIVE STATISTICS
        # =================================================

        st.write("### 📊 Descriptive Statistics")

        statistics = profile["statistics"]

        if not statistics.empty:

            st.dataframe(
                statistics,
                use_container_width=True
            )

        else:

            st.info(
                "No numerical columns available "
                "for descriptive statistics."
            )


        # =================================================
        # DATA PREPROCESSING
        # =================================================

        st.divider()

        st.subheader("🧹 Data Preprocessing")

        processed_df, preprocessing_info = preprocess_dataset(df)


        # =================================================
        # PREPROCESSING SUMMARY
        # =================================================

        st.write("### 📌 Preprocessing Summary")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Original Rows",
                preprocessing_info["original_rows"]
            )

        with col2:

            st.metric(
                "Processed Rows",
                preprocessing_info["processed_rows"]
            )

        with col3:

            st.metric(
                "Duplicates Removed",
                preprocessing_info["duplicates_removed"]
            )


        # =================================================
        # MISSING VALUE SUMMARY
        # =================================================

        col4, col5 = st.columns(2)

        with col4:

            st.metric(
                "Missing Values Before",
                preprocessing_info["missing_values_before"]
            )

        with col5:

            st.metric(
                "Missing Values After",
                preprocessing_info["missing_values_after"]
            )


        # =================================================
        # CLEANED DATASET
        # =================================================

        st.write("### 🧼 Cleaned Dataset")

        st.dataframe(
            processed_df.head(10),
            use_container_width=True
        )


        # =================================================
        # PREPROCESSING COMPLETED MESSAGE
        # =================================================

        if preprocessing_info["missing_values_after"] == 0:

            st.success(
                "✅ Data preprocessing completed successfully. "
                "No missing values remain in the processed dataset."
            )

        else:

            st.warning(
                "⚠️ Some missing values remain after preprocessing."
            )


        # =================================================
        # ASKDATA AI QUERY ENGINE
        # =================================================

        st.divider()

        st.subheader("💬 Ask a Question")

        st.write(
            "Ask a question about your uploaded dataset."
        )


        # -------------------------------------------------
        # USER QUERY
        # -------------------------------------------------

        user_query = st.text_input(
            "Enter your question:",
            placeholder="Example: How many rows are there?"
        )


        # -------------------------------------------------
        # PROCESS USER QUERY
        # -------------------------------------------------

        if user_query:

            result = process_query(
                processed_df,
                user_query
            )


            # ---------------------------------------------
            # TEXT RESULT
            # ---------------------------------------------

            if result["type"] == "text":

                st.info(
                    result["result"]
                )


            # ---------------------------------------------
            # SUMMARY RESULT
            # ---------------------------------------------

            elif result["type"] == "summary":

                summary = result["result"]

                st.write("### 📊 Dataset Summary")

                st.write(
                    f"**Rows:** {summary['rows']}"
                )

                st.write(
                    f"**Columns:** {summary['columns']}"
                )

                st.write(
                    "**Column Names:**"
                )

                st.write(
                    summary["column_names"]
                )

                st.write(
                    "**Numerical Columns:**"
                )

                st.write(
                    summary["numerical_columns"]
                )

                st.write(
                    "**Categorical Columns:**"
                )

                st.write(
                    summary["categorical_columns"]
                )


            # ---------------------------------------------
            # DATAFRAME RESULT
            # ---------------------------------------------

            elif result["type"] == "dataframe":

                st.write("### 📊 Result")

                st.dataframe(
                    result["result"],
                    use_container_width=True
                )


            # ---------------------------------------------
            # ERROR RESULT
            # ---------------------------------------------

            elif result["type"] == "error":

                st.warning(
                    result["result"]
                )
