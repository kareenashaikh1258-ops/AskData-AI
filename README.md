# 📊 AskData AI

### Intelligent Data Analyst Assistant

AskData AI is an intelligent data analysis application that allows users to upload datasets and ask questions in natural language.

The system analyzes the uploaded dataset dynamically and provides answers, summaries, calculations, and analytical results without being hard-coded for a specific dataset.

---

## 📌 Project Overview

Data analysis often requires knowledge of programming, SQL, spreadsheets, or data visualization tools. AskData AI aims to make basic data analysis easier by allowing users to interact with their datasets using natural-language questions.

Users can upload CSV or Excel datasets and ask questions such as:

* What is the average purchase amount?
* What is the total sales?
* Which category has the highest sales?
* Show the top 10 customers by spending.
* What is the average sales by category?
* How many rows are in the dataset?

The application automatically identifies relevant columns and performs the required analysis.

---

## 🎯 Project Objective

The main objective of AskData AI is to develop a user-friendly intelligent data analyst assistant that can:

* Upload CSV and Excel datasets.
* Analyze different datasets dynamically.
* Identify numerical and categorical columns.
* Understand basic natural-language analytical questions.
* Perform calculations such as average, total, maximum, minimum, and count.
* Perform grouped analysis.
* Find top and bottom records or groups.
* Provide dataset summaries and useful insights.

The project is designed to work with different datasets instead of being limited to one specific dataset.

---

## ✨ Features

### 📂 Dataset Upload

* Supports CSV files.
* Supports Excel (`.xlsx`) files.
* Dynamically loads uploaded datasets.

### 📊 Dataset Analysis

* Displays dataset preview.
* Shows the number of rows and columns.
* Identifies numerical columns.
* Identifies categorical columns.
* Provides basic dataset information.

### 💬 Natural Language Query Engine

Users can ask questions such as:

* Average of a numerical column.
* Total or sum of a numerical column.
* Maximum and minimum values.
* Record counts.
* Grouped averages.
* Grouped totals.
* Grouped counts.
* Top N analysis.
* Bottom N analysis.
* Dataset summary questions.

### 🔍 Dynamic Column Detection

The Query Engine attempts to identify relevant columns dynamically based on the user's question.

For example, it can identify concepts such as:

* Sales
* Revenue
* Purchase Amount
* Spending
* Profit
* Salary
* Price
* Rating
* Quantity
* Age
* Customer
* Product
* Category
* Location
* Gender

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Pandas**
* **NumPy**
* **OpenPyXL**
* **Regular Expressions (re)**

---

## 🏗️ System Architecture

```text
                ┌──────────────────┐
                │      User        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Streamlit UI   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  Dataset Upload  │
                │   CSV / XLSX     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Data Loader    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Data Preprocessor│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Dataset Profiler │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │   Query Engine   │
                │ Natural Language │
                │    Processing    │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Analysis Result  │
                └──────────────────┘
```

---

## 📁 Project Directory Structure

```text
ask_data_ai/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── AskData_AI_Project_Synopsis (2).pdf
├── PRD.docx
├── Functional Requirements Document.docx
├── Technical Requirements Document (TRD) — AskData AI.docx
├── AskData_AI_Directory_Structure.docx
│
└── modules/
    │
    ├── __init__.py
    ├── data_loader.py
    ├── profiler.py
    ├── preprocessor.py
    └── query_engine.py
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/kareenashaikh1258-ops/AskData-AI.git
```

### 2. Open the project folder

```bash
cd AskData-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```bash
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

Run the following command:

```bash
streamlit run app.py
```

Then open the Streamlit application in your browser.

---

## 💬 Example Queries

AskData AI supports questions such as:

```text
What is the average purchase amount?
```

```text
What is the total sales?
```

```text
What is the highest revenue?
```

```text
What is the minimum salary?
```

```text
How many rows are in the dataset?
```

```text
How many columns are in the dataset?
```

```text
What is the average sales by category?
```

```text
What is the total revenue by location?
```

```text
Show the top 10 customers by spending.
```

```text
Show the bottom 5 products by sales.
```

---

## 📊 Supported Dataset Types

Currently supported:

* CSV (`.csv`)
* Excel (`.xlsx`)

AskData AI is designed to analyze uploaded datasets dynamically. It is not dependent on one fixed dataset.

For best results, datasets should contain:

* Column headers.
* Structured tabular data.
* Numerical columns for calculations.
* Categorical columns for grouped analysis.

---

## 🧠 Query Processing Workflow

When a user enters a question, the Query Engine follows these general steps:

```text
User Question
      ↓
Text Normalization
      ↓
Operation Detection
      ↓
Column Detection
      ↓
Metric Identification
      ↓
Group Detection
      ↓
Top / Bottom Detection
      ↓
Data Analysis
      ↓
Result Display
```

For example:

```text
Question:
"Show the top 10 customers by spending"
```

The system attempts to identify:

```text
Group Column  → Customer
Metric        → Purchase Amount / Spending
Operation     → Total
Limit         → 10
Direction     → Top
```

Then it performs the analysis dynamically based on the uploaded dataset.

---

## 🚀 Future Enhancements

Future versions of AskData AI can include:

* Advanced filtering using natural-language questions.
* Multiple-condition queries.
* Automatic chart generation.
* Data visualization dashboard.
* Correlation analysis.
* Outlier detection.
* Trend analysis.
* Automatic insight generation.
* Support for date-based analysis.
* Support for more file formats.
* SQL database connectivity.
* Natural Language Processing (NLP) improvements.
* Retrieval-Augmented Generation (RAG).
* Integration with free and locally deployable LLM models.
* More advanced conversational data analysis.

---

## 🎓 Project Type

**TY B.Sc. Data Science — College Final Year Project**

This project is being developed as an intelligent and adaptable data analysis assistant for analyzing different user-uploaded datasets through natural-language interaction.

---

## 👩‍💻 Author

**Kareena Shaikh**

TY B.Sc. Data Science Student
Aspiring Data Analyst

### Skills

* Python
* SQL
* Power BI
* Tableau
* Data Analysis
* Data Visualization
* Machine Learning
* Pandas

---

## 📌 Project Status

🚧 **Currently Under Development**

The project currently supports dataset uploading, preprocessing, profiling, and basic natural-language analytical queries. Advanced query understanding and additional analytics features are being actively developed.
