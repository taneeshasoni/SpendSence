import streamlit as st
import sqlite3
import hashlib


# ================= DATABASE =================

def get_connection():
    return sqlite3.connect(
        "spendsense.db",
        check_same_thread=False
    )


# ================= PASSWORD HASHING =================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ================= CREATE USERS TABLE =================

def create_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ================= SIGN UP =================

def signup_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            hash_password(password)
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


# ================= LOGIN =================

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM users
        WHERE email = ? AND password = ?
    """, (
        email,
        hash_password(password)
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# ================= AUTH PAGE =================

def show_auth_page():

    st.markdown("""
    <style>

    .auth-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #F1DEC4;
    }

    .auth-subtitle {
        text-align: center;
        color: #9CB080;
        font-size: 18px;
        margin-bottom: 30px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="auth-title">💰 SpendSence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="auth-subtitle">Track your money. Build your future.</div>',
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "✨ Sign Up"]
    )


    # ================= LOGIN =================

    with login_tab:

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        if st.button(
            "LOGIN",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter email and password."
                )

            else:

                user = login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]

                    st.success(
                        f"Welcome back, {user[1]}! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )


    # ================= SIGN UP =================

    with signup_tab:

        name = st.text_input(
            "Full Name",
            placeholder="Enter your name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password",
            key="confirm_password"
        )

        if st.button(
            "CREATE ACCOUNT",
            use_container_width=True
        ):

            if not name or not email or not password or not confirm_password:

                st.warning(
                    "Please fill all fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            else:

                success = signup_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Account created successfully! 🎉 "
                        "Now you can login."
                    )

                else:

                    st.error(
                        "This email is already registered."
                    )