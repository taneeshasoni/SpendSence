import streamlit as st
import pandas as pd


def show_import_data():

    st.title("📂 Import & Analyse Data")
    st.write("Upload your expense data using CSV or Excel.")

    # =====================================================
    # FILE UPLOAD
    # =====================================================

    uploaded_file = st.file_uploader(
        "Upload your expense file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is None:
        st.info("Please upload a CSV or Excel file to continue.")
        return

    # =====================================================
    # READ FILE
    # =====================================================

    try:

        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(f"Unable to read the file: {e}")
        return

    # =====================================================
    # PREVIEW
    # =====================================================

    st.subheader("📋 Imported Data")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    st.subheader("📊 Quick Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    # Find amount column
    amount_column = None

    for column in df.columns:

        if column.lower() in [
            "amount",
            "expense",
            "expenses",
            "price",
            "cost"
        ]:
            amount_column = column
            break

    if amount_column is None:

        st.warning(
            "I couldn't find an Amount column. "
            "Please name your amount column as 'Amount'."
        )

        return

    # Convert amount to numbers
    df[amount_column] = pd.to_numeric(
        df[amount_column],
        errors="coerce"
    )

    df = df.dropna(
        subset=[amount_column]
    )

    total_expense = df[amount_column].sum()
    average_expense = df[amount_column].mean()
    highest_expense = df[amount_column].max()

    with col2:
        st.metric(
            "Total Expense",
            f"₹{total_expense:,.2f}"
        )

    with col3:
        st.metric(
            "Average Expense",
            f"₹{average_expense:,.2f}"
        )

    with col4:
        st.metric(
            "Highest Expense",
            f"₹{highest_expense:,.2f}"
        )

    # =====================================================
    # CATEGORY ANALYSIS
    # =====================================================

    category_column = None

    for column in df.columns:

        if column.lower() in [
            "category",
            "type"
        ]:
            category_column = column
            break

    if category_column:

        st.subheader("💸 Expense by Category")

        category_expense = (
            df.groupby(category_column)[amount_column]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(category_expense)

        st.subheader("📋 Category Summary")

        category_table = category_expense.reset_index()

        category_table.columns = [
            "Category",
            "Total Expense"
        ]

        st.dataframe(
            category_table,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # DATE ANALYSIS
    # =====================================================

    date_column = None

    for column in df.columns:

        if column.lower() in [
            "date",
            "expense date",
            "transaction date"
        ]:
            date_column = column
            break

    if date_column:

        df[date_column] = pd.to_datetime(
            df[date_column],
            errors="coerce"
        )

        df = df.dropna(
            subset=[date_column]
        )

        df["Month"] = df[date_column].dt.strftime(
            "%B %Y"
        )

        monthly_expense = (
            df.groupby("Month")[amount_column]
            .sum()
        )

        st.subheader("📅 Monthly Expense")

        st.bar_chart(monthly_expense)

    # =====================================================
    # EXPENSE TREND
    # =====================================================

    if date_column:

        daily_expense = (
            df.groupby(date_column)[amount_column]
            .sum()
        )

        st.subheader("📈 Expense Trend")

        st.line_chart(daily_expense)

    # =====================================================
    # DOWNLOAD CLEANED DATA
    # =====================================================

    st.subheader("💾 Export Data")

    csv_data = df.to_csv(
        index=False
    )

    st.download_button(
        "⬇️ Download Analysed Data",
        csv_data,
        "spendsense_analysis.csv",
        "text/csv"
    )