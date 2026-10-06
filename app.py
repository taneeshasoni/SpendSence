from import_data import show_import_data
import streamlit as st
from auth import create_users_table, show_auth_page
import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import plotly.express as px

create_users_table()

# Initialize login state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Show login/signup if user is not logged in
if not st.session_state.logged_in:

    show_auth_page()

    st.stop()

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="SpendSense",
    page_icon="💰",
    layout="wide"
)
# =========================================================
# PAGE NAVIGATION
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if st.session_state.page == "import":
    show_import_data()
    st.stop()
# =========================================================
# SPENDSENSE THEME
# =========================================================

st.markdown("""
<style>

   /* ==========================================
    FORM LABELS
    ========================================== */

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stDateInput label {
    color: #092328 !important;
    font-weight: 600 !important;
    }

    /* Income heading / text */
    h1, h2, h3, h4, h5, h6 {
    color: #092328 !important;
    }

   /* Normal markdown text */
   .stMarkdown p {
   color: #092328 !important;
    }

    /* ==========================================
       MAIN APP
       ========================================== */

    .stApp {
        background-color: #9CB080;
        color: #092328;
    }


    /* ==========================================
       SIDEBAR
       ========================================== */

    [data-testid="stSidebar"] {
        background-color: #092328;
    }

    [data-testid="stSidebar"] * {
        color: #F1DEC4 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #49666A;
    }


    /* ==========================================
       HEADINGS
       ========================================== */

    h1 {
        color: #092328 !important;
        font-weight: 700 !important;
    }

    h2 {
        color: #092328 !important;
        font-weight: 650 !important;
    }

    h3 {
        color: #092328 !important;
        font-weight: 600 !important;
    }


    /* ==========================================
       METRIC CARDS
       ========================================== */

    [data-testid="stMetric"] {
        background-color: #092328;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #49666A;
        box-shadow: 0 4px 12px rgba(9, 35, 40, 0.12);
    }

    [data-testid="stMetricLabel"] {
        color: #F1DEC4 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F1DEC4 !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #B99B7D !important;
    }


    /* ==========================================
       BUTTONS
       ========================================== */

    .stButton > button {
        background-color: #092328;
        color: #F1DEC4;
        border: 1px solid #092328;
        border-radius: 10px;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #49666A;
        color: #F1DEC4;
        border-color: #49666A;
    }


    /* ==========================================
       INPUT BOXES
       ========================================== */

    .stTextInput input,
    .stNumberInput input {
        background-color: #FFFFFF;
        color: #092328;
        border: 1px solid #B99B7D;
        border-radius: 10px;
    }


    /* ==========================================
       SELECT BOX
       ========================================== */

    [data-baseweb="select"] > div {
        background-color: #FFFFFF;
        border: 1px solid #B99B7D;
        border-radius: 10px;
    }


    /* ==========================================
       DATE INPUT
       ========================================== */

    [data-testid="stDateInput"] input {
        background-color: #FFFFFF;
        color: #092328;
        border: 1px solid #B99B7D;
        border-radius: 10px;
    }


    /* ==========================================
       DATAFRAME
       ========================================== */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }


    /* ==========================================
       SUCCESS MESSAGE
       ========================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ==========================================
       DIVIDERS
       ========================================== */

    hr {
        border-color: #D8C4AC;
    }


    /* ==========================================
       SIDEBAR HISTORY BUTTONS
       ========================================== */

    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent;
        color: #F1DEC4 !important;
        border: 1px solid #49666A;
        text-align: left;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #49666A;
        border-color: #F1DEC4;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
    background-color: #49666A;
    border-color: #F1DEC4;
}


/* =====================================================
   ADD EXPENSE BOXES
   ===================================================== */

.stSelectbox [data-baseweb="select"] > div,
.stNumberInput input,
.stDateInput input,
.stTextInput input {
    background-color: #092328 !important;
    color: #9CB080 !important;
    -webkit-text-fill-color: #9CB080 !important;
}

/* Category selected text */
.stSelectbox [data-baseweb="select"] span {
    color: #9CB080 !important;
}

/* Placeholder text */
.stTextInput input::placeholder {
    color: #9CB080 !important;
    -webkit-text-fill-color: #9CB080 !important;
    opacity: 1 !important;
}

/* Date calendar icon */
.stDateInput svg {
    fill: #9CB080 !important;
}

/* Number +/- buttons */
.stNumberInput button {
    background-color: #092328 !important;
    color: #9CB080 !important;
}

.stNumberInput button svg {
    fill: #9CB080 !important;
}





</style>
""", unsafe_allow_html=True)
# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "spendsense.db",
    check_same_thread=False
)

cursor = conn.cursor()


# =========================================================
# CREATE TABLES
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    amount REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    month TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT
)
""")

conn.commit()


# =========================================================
# MONTHS
# =========================================================

months = [
    "January", "February", "March",
    "April", "May", "June",
    "July", "August", "September",
    "October", "November", "December"
]

current_year = date.today().year
current_month = date.today().month

month_numbers = {month: i + 1 for i, month in enumerate(months)}


# =========================================================
# SESSION STATE
# =========================================================

if "selected_month" not in st.session_state:
    st.session_state.selected_month = (
        f"{months[current_month - 1]} {current_year}"
    )


# =========================================================
# SIDEBAR
# =========================================================

col1, col2 = st.columns([8, 1])

with col1:
    st.title("SpendSense")

with col2:
    save = st.button("💾 Save", use_container_width=True)

if save:
    st.toast("Saved successfully! ✅", icon="💾")

    # Import Data option
if st.sidebar.button("📂 Import Data", use_container_width=True):
    st.session_state.page = "import"

st.sidebar.divider()

st.sidebar.subheader("📅 Current Month")

selected_month_name = st.sidebar.selectbox(
    "Select month",
    months,
    index=month_numbers[
        st.session_state.selected_month.split()[0]
    ] - 1
)

selected_month = f"{selected_month_name} {current_year}"

st.session_state.selected_month = selected_month


# =========================================================
# HISTORY
# =========================================================

st.sidebar.divider()
st.sidebar.subheader("📚 History")

history_df = pd.read_sql_query(
    """
    SELECT DISTINCT month
    FROM (
        SELECT month FROM income
        UNION
        SELECT month FROM expenses
    )
    """,
    conn
)

history_months = history_df["month"].tolist()


if history_months:

    # Sort newest first
    history_months = sorted(
        history_months,
        key=lambda x: (
            int(x.split()[1]),
            month_numbers[x.split()[0]]
        ),
        reverse=True
    )

    for history_month in history_months:

        if st.sidebar.button(
            f"📅 {history_month}",
            key=f"history_{history_month}",
            use_container_width=True
        ):
            st.session_state.selected_month = history_month
            st.rerun()

else:

    st.sidebar.info(
        "Your previous months will appear here."
    )


# =========================================================
# MAIN TITLE
# =========================================================

st.title("💰 SpendSense")

st.caption(
    f"Personal Finance Dashboard • {st.session_state.selected_month}"
)


# =========================================================
# GET SELECTED MONTH
# =========================================================

selected_month = st.session_state.selected_month


# =========================================================
# ADD INCOME
# =========================================================

st.subheader("💵 Add Monthly Income")

col1, col2 = st.columns([2, 1])

with col1:

    income_amount = st.number_input(
        f"Income for {selected_month}",
        min_value=0.0,
        step=100.0,
        format="%.2f",
        key=f"income_input_{selected_month}"
    )

with col2:

    st.write("")
    st.write("")

    if st.button(
        "💾 Save Income",
        use_container_width=True
    ):

        if income_amount > 0:

            cursor.execute(
                """
                INSERT INTO income
                (month, amount)
                VALUES (?, ?)
                """,
                (
                    selected_month,
                    income_amount
                )
            )

            conn.commit()

            st.success(
                f"₹{income_amount:,.2f} saved for {selected_month}"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter an income greater than ₹0."
            )


# =========================================================
# ADD EXPENSE
# =========================================================

st.divider()

st.subheader("💸 Add Expense")

categories = [
    "Food",
    "Rent",
    "Electricity",
    "Water Bill",
    "Travel Expense",
    "Health",
    "Shopping",
    "EMI",
    "Other"
]

col1, col2 = st.columns(2)

with col1:

    expense_category = st.selectbox(
        "Category",
        categories
    )

    expense_amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=50.0,
        format="%.2f"
    )

with col2:

    expense_date = st.date_input(
        "Expense Date",
        value=date.today()
    )

    expense_description = st.text_input(
        "Description",
        placeholder="e.g. Groceries, bus ticket..."
    )


if st.button(
    "💾 Save Expense",
    use_container_width=True
):

    if expense_amount > 0:

        cursor.execute(
            """
            INSERT INTO expenses
            (date, month, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                str(expense_date),
                selected_month,
                expense_category,
                expense_amount,
                expense_description
            )
        )

        conn.commit()

        st.success(
            f"₹{expense_amount:,.2f} added to {selected_month}"
        )

        st.rerun()

    else:

        st.warning(
            "Please enter an expense greater than ₹0."
        )


# =========================================================
# MONTHLY DATA
# =========================================================

income_result = cursor.execute(
    """
    SELECT SUM(amount)
    FROM income
    WHERE month = ?
    """,
    (selected_month,)
).fetchone()

total_income = income_result[0] or 0


expense_result = cursor.execute(
    """
    SELECT SUM(amount)
    FROM expenses
    WHERE month = ?
    """,
    (selected_month,)
).fetchone()

total_expense = expense_result[0] or 0


savings = total_income - total_expense


# =========================================================
# DASHBOARD
# =========================================================

st.divider()

st.header(
    f"📊 {selected_month} Dashboard"
)


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "💰 Total Income",
        f"₹{total_income:,.2f}"
    )

with col2:

    st.metric(
        "💸 Total Spent",
        f"₹{total_expense:,.2f}"
    )

with col3:

    st.metric(
        "💵 Savings",
        f"₹{savings:,.2f}"
    )


# =========================================================
# =========================================================
# SAVINGS MESSAGE
# =========================================================

if total_income > 0:

    saving_percentage = (
        savings / total_income
    ) * 100

    if savings > 0:

        st.markdown(
            f"""
            <div style="
                background-color: #092328;
                color: #F1DEC4;
                padding: 18px 22px;
                border-radius: 14px;
                border: 2px solid #618764;
                font-size: 17px;
                font-weight: 600;
                margin: 10px 0;
            ">
                🎉 You saved ₹{savings:,.2f}
                ({saving_percentage:.1f}% of your income)
            </div>
            """,
            unsafe_allow_html=True
        )

    elif savings == 0:

        st.markdown(
            """
            <div style="
                background-color: #F1DEC4;
                color: #092328;
                padding: 18px 22px;
                border-radius: 14px;
                border: 2px solid #9CB080;
                font-size: 17px;
                font-weight: 600;
                margin: 10px 0;
            ">
                💰 You have used your entire income this month.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div style="
                background-color: #092328;
                color: #F1DEC4;
                padding: 18px 22px;
                border-radius: 14px;
                border: 2px solid #B99B7D;
                font-size: 17px;
                font-weight: 600;
                margin: 10px 0;
            ">
                ⚠️ You spent ₹{abs(savings):,.2f}
                more than your income.
            </div>
            """,
            unsafe_allow_html=True
        )
# =========================================================
# CATEGORY DATA
# =========================================================

category_df = pd.read_sql_query(
    """
    SELECT
        category,
        SUM(amount) AS amount
    FROM expenses
    WHERE month = ?
    GROUP BY category
    ORDER BY amount DESC
    """,
    conn,
    params=(selected_month,)
)


# =========================================================
# CHARTS
# =========================================================

if not category_df.empty:

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Spending by Category")

        fig_category = px.bar(
            category_df,
            x="category",
            y="amount",
            title="Where is your money going?",
            labels={
                "category": "Category",
                "amount": "Amount (₹)"
            }
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    with col2:

        st.subheader("🥧 Expense Distribution")

        fig_pie = px.pie(
            category_df,
            names="category",
            values="amount",
            title="Expense Distribution"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )


# =========================================================
# MONTHLY EXPENSE LIST
# =========================================================

st.divider()

st.subheader(
    f"🧾 {selected_month} Expenses"
)


expenses_df = pd.read_sql_query(
    """
    SELECT
        id,
        date,
        category,
        amount,
        description
    FROM expenses
    WHERE month = ?
    ORDER BY date DESC
    """,
    conn,
    params=(selected_month,)
)


if not expenses_df.empty:

    display_df = expenses_df.copy()

    display_df["amount"] = display_df[
        "amount"
    ].apply(
        lambda x: f"₹{x:,.2f}"
    )

    display_df = display_df.rename(
        columns={
            "id": "ID",
            "date": "Date",
            "category": "Category",
            "amount": "Amount",
            "description": "Description"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No expenses recorded for this month."
    )


# =========================================================
# DELETE EXPENSE
# =========================================================

if not expenses_df.empty:

    st.subheader("🗑️ Delete Expense")

    expense_ids = expenses_df["id"].tolist()

    selected_expense_id = st.selectbox(
        "Select expense ID",
        expense_ids
    )

    if st.button(
        "🗑️ Delete Selected Expense"
    ):

        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (selected_expense_id,)
        )

        conn.commit()

        st.success(
            "Expense deleted successfully."
        )

        st.rerun()


# =========================================================
# INCOME HISTORY
# =========================================================

st.divider()

st.subheader(
    f"💰 Income History — {selected_month}"
)


income_df = pd.read_sql_query(
    """
    SELECT
        id,
        month,
        amount
    FROM income
    WHERE month = ?
    ORDER BY id DESC
    """,
    conn,
    params=(selected_month,)
)


if not income_df.empty:

    income_display = income_df.copy()

    income_display["amount"] = income_display[
        "amount"
    ].apply(
        lambda x: f"₹{x:,.2f}"
    )

    income_display = income_display.rename(
        columns={
            "id": "ID",
            "month": "Month",
            "amount": "Income"
        }
    )

    st.dataframe(
        income_display,
        use_container_width=True,
        hide_index=True
    )


    income_ids = income_df["id"].tolist()

    selected_income_id = st.selectbox(
        "Select income ID to delete",
        income_ids
    )

    if st.button(
        "🗑️ Delete Selected Income"
    ):

        cursor.execute(
            """
            DELETE FROM income
            WHERE id = ?
            """,
            (selected_income_id,)
        )

        conn.commit()

        st.success(
            "Income deleted successfully."
        )

        st.rerun()

else:

    st.info(
        "No income recorded for this month."
    )


# =========================================================
# LAST 3 MONTHS COMPARISON
# =========================================================

st.divider()

st.header("📈 Monthly Comparison")

comparison_df = pd.read_sql_query(
    """
    SELECT
        month,
        SUM(income) AS income,
        SUM(expense) AS expense
    FROM (
        SELECT
            month,
            amount AS income,
            0 AS expense
        FROM income

        UNION ALL

        SELECT
            month,
            0 AS income,
            amount AS expense
        FROM expenses
    )
    GROUP BY month
    """,
    conn
)


if not comparison_df.empty:

    comparison_df["savings"] = (
        comparison_df["income"]
        - comparison_df["expense"]
    )


    comparison_df["month_number"] = (
        comparison_df["month"]
        .apply(
            lambda x: month_numbers[
                x.split()[0]
            ]
        )
    )


    comparison_df = comparison_df.sort_values(
        ["month_number"]
    )


    # Last 3 available months
    comparison_df = comparison_df.tail(3)


    chart_df = comparison_df[
        ["month", "income", "expense", "savings"]
    ]


    fig_comparison = px.bar(
        chart_df,
        x="month",
        y=[
            "income",
            "expense",
            "savings"
        ],
        barmode="group",
        title="Income vs Expenses vs Savings",
        labels={
            "value": "Amount (₹)",
            "month": "Month",
            "variable": "Type"
        }
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )

else:

    st.info(
        "Add data for multiple months to see the comparison."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "💰 SpendSense • Your personal finance tracker"
)


# =========================================================
# CLOSE DATABASE
# =========================================================

conn.close() 