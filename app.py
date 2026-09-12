
import pandas as pd
import streamlit as st

from modules.data_loader import load_dataset
from modules.profiler import profile_dataset
from modules.preprocessor import preprocess_dataset
from modules.query_engine import process_query


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AskData AI",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("📊 AskData AI")

st.subheader("Intelligent Data Analyst Assistant")

st.write(
    "Upload your dataset and ask questions using natural language."
)

st.divider()


# =========================================================
# FILE UPLOADER
# =========================================================

uploaded_file = st.file_uploader(
    "📁 Upload your CSV or Excel dataset",
    type=["csv", "xlsx"]
)


# =========================================================
# NO FILE UPLOADED
# =========================================================

if uploaded_file is None:

    st.info(
        "👆 Please upload a CSV or Excel dataset to get started."
    )

    st.write("## 🚀 How AskData AI Works")

    st.write("1. Upload a CSV or Excel dataset")
    st.write("2. Preview your dataset")
    st.write("3. Automatically profile the data")
    st.write("4. Preprocess the data")
    st.write("5. Ask questions in natural language")
    st.write("6. Get analytical results")

    st.write("## 💡 Example Questions")

    col1, col2 = st.columns(2)

    with col1:
        st.write("• What is the average value?")
        st.write("• What is the total value?")
        st.write("• What is the highest value?")
        st.write("• What is the lowest value?")

    with col2:
        st.write("• Show top 10 records")
        st.write("• Show top 10 customers by spending")
        st.write("• What is the average value by category?")
        st.write("• Give me a summary of the dataset")


# =========================================================
# FILE UPLOADED
# =========================================================

else:

    # =====================================================
    # LOAD DATASET
    # =====================================================

    try:

        loaded_data = load_dataset(uploaded_file)

        # -------------------------------------------------
        # IMPORTANT:
        # load_dataset() may return:
        #
        # 1. A DataFrame
        # OR
        # 2. A tuple containing a DataFrame
        #
        # We handle both cases here.
        # -------------------------------------------------

        if isinstance(loaded_data, tuple):

            # Find the DataFrame inside the tuple
            df = None

            for item in loaded_data:

                if isinstance(item, pd.DataFrame):
                    df = item
                    break

            if df is None:

                st.error(
                    "The dataset loader returned a tuple, "
                    "but no DataFrame was found inside it."
                )

                st.stop()

        elif isinstance(loaded_data, pd.DataFrame):

            df = loaded_data

        else:

            st.error(
                "The dataset loader did not return a valid DataFrame."
            )

            st.stop()


        # -------------------------------------------------
        # CHECK EMPTY DATASET
        # -------------------------------------------------

        if df.empty:

            st.error(
                "The uploaded dataset is empty."
            )

            st.stop()


        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        st.success(
            "Dataset loaded successfully! ✅"
        )


    except Exception as e:

        st.error(
            f"Error while loading dataset: {e}"
        )

        st.stop()


    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    st.header("📊 Dataset Overview")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Rows",
            df.shape[0]
        )


    with col2:

        st.metric(
            "Columns",
            df.shape[1]
        )


    with col3:

        st.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )


    with col4:

        st.metric(
            "Duplicate Rows",
            int(df.duplicated().sum())
        )


    # =====================================================
    # DATASET PREVIEW
    # =====================================================

    st.header("👀 Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


    # =====================================================
    # COMPLETE COLUMN LIST
    # =====================================================

    with st.expander("📋 View All Columns"):

        for i, column in enumerate(df.columns, start=1):

            st.write(
                f"{i}. {column}"
            )


    # =====================================================
    # DATASET PROFILING
    # =====================================================

    st.header("🔍 Dataset Profiling")


    try:

        profile = profile_dataset(df)


        # -------------------------------------------------
        # IF PROFILE IS A DICTIONARY
        # -------------------------------------------------

        if isinstance(profile, dict):


            # ---------------------------------------------
            # BASIC PROFILE INFORMATION
            # ---------------------------------------------

            profile_col1, profile_col2 = st.columns(2)


            with profile_col1:

                st.write("### 🔢 Numerical Columns")

                numeric_columns = profile.get(
                    "numeric_columns",
                    []
                )

                st.write(numeric_columns)


            with profile_col2:

                st.write("### 🔤 Categorical Columns")

                categorical_columns = profile.get(
                    "categorical_columns",
                    []
                )

                st.write(categorical_columns)


            # ---------------------------------------------
            # DATA TYPES
            # ---------------------------------------------

            if "dtypes" in profile:

                st.write("### 🧾 Data Types")

                st.write(
                    profile["dtypes"]
                )


            # ---------------------------------------------
            # MISSING VALUES
            # ---------------------------------------------

            if "missing_values" in profile:

                st.write("### ❓ Missing Values")

                st.write(
                    profile["missing_values"]
                )


            # ---------------------------------------------
            # UNIQUE VALUES
            # ---------------------------------------------

            if "unique_values" in profile:

                st.write("### 🔢 Unique Values")

                st.write(
                    profile["unique_values"]
                )


            # ---------------------------------------------
            # DESCRIPTIVE STATISTICS
            # ---------------------------------------------

            if "descriptive_statistics" in profile:

                st.write(
                    "### 📈 Descriptive Statistics"
                )

                stats = profile[
                    "descriptive_statistics"
                ]

                if isinstance(stats, pd.DataFrame):

                    st.dataframe(
                        stats,
                        use_container_width=True
                    )

                else:

                    st.write(stats)


        else:

            st.info(
                "Dataset profiling completed."
            )


    except Exception as e:

        st.warning(
            f"Profiling could not be completed: {e}"
        )


    # =====================================================
    # DATA PREPROCESSING
    # =====================================================

    st.header("🧹 Data Preprocessing")


    try:

        processed_data = preprocess_dataset(df)


        # -------------------------------------------------
        # PREPROCESSOR MAY RETURN A TUPLE
        # -------------------------------------------------

        if isinstance(processed_data, tuple):

            processed_df = None

            for item in processed_data:

                if isinstance(item, pd.DataFrame):

                    processed_df = item
                    break


            if processed_df is None:

                st.warning(
                    "Preprocessing did not return a DataFrame. "
                    "The original dataset will be used."
                )

                processed_df = df.copy()


        elif isinstance(processed_data, pd.DataFrame):

            processed_df = processed_data


        else:

            st.warning(
                "Preprocessing did not return a valid DataFrame. "
                "The original dataset will be used."
            )

            processed_df = df.copy()


        # -------------------------------------------------
        # EMPTY PROCESSED DATASET CHECK
        # -------------------------------------------------

        if processed_df.empty:

            st.warning(
                "The processed dataset is empty. "
                "The original dataset will be used."
            )

            processed_df = df.copy()


        st.success(
            "Data preprocessing completed successfully! ✅"
        )


        # -------------------------------------------------
        # PREPROCESSING INFORMATION
        # -------------------------------------------------

        prep_col1, prep_col2, prep_col3 = st.columns(3)


        with prep_col1:

            st.metric(
                "Original Rows",
                df.shape[0]
            )


        with prep_col2:

            st.metric(
                "Processed Rows",
                processed_df.shape[0]
            )


        with prep_col3:

            st.metric(
                "Processed Columns",
                processed_df.shape[1]
            )


        # -------------------------------------------------
        # VIEW PROCESSED DATA
        # -------------------------------------------------

        with st.expander(
            "👀 View Processed Dataset"
        ):

            st.dataframe(
                processed_df.head(20),
                use_container_width=True
            )


    except Exception as e:

        st.warning(
            f"Preprocessing could not be completed: {e}"
        )

        processed_df = df.copy()


    # =====================================================
    # NATURAL LANGUAGE QUERY SECTION
    # =====================================================

    st.divider()

    st.header("💬 AskData AI")

    st.write(
        "Ask a question about your uploaded dataset "
        "using simple English."
    )


    # =====================================================
    # EXAMPLE QUESTIONS
    # =====================================================

    st.write("### 💡 Example Questions")


    example_col1, example_col2 = st.columns(2)


    with example_col1:

        st.write(
            "• What is the average purchase amount?"
        )

        st.write(
            "• What is the total sales?"
        )

        st.write(
            "• What is the highest value?"
        )

        st.write(
            "• What is the lowest value?"
        )


    with example_col2:

        st.write(
            "• Show top 10 customers by spending."
        )

        st.write(
            "• What is the average value by category?"
        )

        st.write(
            "• Show the top 5 records."
        )

        st.write(
            "• Give me a summary of the dataset."
        )


    # =====================================================
    # QUERY INPUT
    # =====================================================

    user_query = st.text_input(
        "🔎 Enter your question:",
        placeholder=(
            "Example: What is the average purchase amount?"
        )
    )


    # =====================================================
    # PROCESS USER QUERY
    # =====================================================

    if user_query.strip() != "":

        with st.spinner(
            "🤖 Analyzing your question..."
        ):

            try:

                result = process_query(
                    processed_df,
                    user_query
                )


                # =================================================
                # RESULT VALIDATION
                # =================================================

                if not isinstance(result, dict):

                    st.error(
                        "The query engine returned an invalid result."
                    )

                    st.write(result)

                    st.stop()


                # =================================================
                # TEXT RESULT
                # =================================================

                if result.get("type") == "text":

                    st.success(
                        result.get(
                            "message",
                            "No result message was returned."
                        )
                    )


                # =================================================
                # DATAFRAME RESULT
                # =================================================

                elif result.get("type") == "dataframe":

                    st.write("### 📋 Query Result")

                    query_data = result.get(
                        "data"
                    )


                    if isinstance(
                        query_data,
                        pd.DataFrame
                    ):

                        st.dataframe(
                            query_data,
                            use_container_width=True
                        )

                    else:

                        st.write(
                            query_data
                        )


                # =================================================
                # SUMMARY RESULT
                # =================================================

                elif result.get("type") == "summary":

                    st.write(
                        "### 📊 Dataset Summary"
                    )


                    summary = result.get(
                        "data",
                        {}
                    )


                    if isinstance(
                        summary,
                        dict
                    ):

                        summary_col1, summary_col2, summary_col3 = (
                            st.columns(3)
                        )


                        with summary_col1:

                            st.metric(
                                "Rows",
                                summary.get(
                                    "rows",
                                    processed_df.shape[0]
                                )
                            )


                        with summary_col2:

                            st.metric(
                                "Columns",
                                summary.get(
                                    "columns",
                                    processed_df.shape[1]
                                )
                            )


                        with summary_col3:

                            st.metric(
                                "Missing Values",
                                summary.get(
                                    "missing_values",
                                    int(
                                        processed_df
                                        .isnull()
                                        .sum()
                                        .sum()
                                    )
                                )
                            )


                        # -----------------------------------------
                        # NUMERICAL COLUMNS
                        # -----------------------------------------

                        st.write(
                            "#### 🔢 Numerical Columns"
                        )

                        st.write(
                            summary.get(
                                "numeric_columns",
                                []
                            )
                        )


                        # -----------------------------------------
                        # CATEGORICAL COLUMNS
                        # -----------------------------------------

                        st.write(
                            "#### 🔤 Categorical Columns"
                        )

                        st.write(
                            summary.get(
                                "categorical_columns",
                                []
                            )
                        )


                    else:

                        st.write(
                            summary
                        )


                # =================================================
                # ERROR RESULT
                # =================================================

                elif result.get("type") == "error":

                    st.error(
                        result.get(
                            "message",
                            "An unknown error occurred."
                        )
                    )


                # =================================================
                # UNKNOWN RESULT TYPE
                # =================================================

                else:

                    st.warning(
                        "The query engine returned an unknown result."
                    )

                    st.write(
                        result
                    )


            except Exception as e:

                st.error(
                    "An error occurred while processing "
                    "your question."
                )

                st.exception(e)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AskData AI | Intelligent Data Analyst Assistant"
)

